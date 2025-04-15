import express from 'express';
import { createServer } from 'node:http';
import { SerialPort, ReadlineParser } from 'serialport';
import { Server } from 'socket.io';
import cors from 'cors'
import { writeFileSync, mkdirSync } from 'node:fs';

const parser = new ReadlineParser({
  delimiter: '\r\n'
});

var port = new SerialPort({
  path: '/dev/cu.usbmodemDC5475E9EE282',
  baudRate: 9600,
  dataBits: 8,
  parity: 'none',
  stopBits: 1,
  flowControl: false
});

port.pipe(parser);


const app = express();
app.use(cors())
const server = createServer(app);
const io = new Server(server, {
    cors: {
    origin: "http://localhost:5173"
  }});


app.get('/', (req, res) => {
  res.send('<h1>Hello world</h1>');
});



let recording = false

let recordingFile = {
  rows: [],
  startTime: Date.now(),
}

let csv = 'Conductance,Timestamp'
csv += '\n'

const handleStartRecording = (timestamp) => {
  recording = true
  recordingFile.startTime = timestamp
  console.log('recording started')
}

const handleStopRecording = () => {
  if(recording){
  
    // Write Records
    const jsonData = JSON.stringify(recordingFile)
    let d = new Date()
    const folderPath = `recordings/recording-${[d.getMonth()+1,d.getDate(),d.getFullYear()].join('-')+[d.getHours(),d.getMinutes(),d.getSeconds()].join('-')}`
    mkdirSync(folderPath,  { recursive: true })
    writeFileSync(`${folderPath}/data.csv`, csv)
    writeFileSync(`${folderPath}/data.json`, jsonData)
    
    // Reset Records
    csv = 'Conductance,Timestamp'
    csv += '\n'

    recordingFile = {
      rows: [],
      startTime: Date.now(),
    }
    recording = false
  }
}

io.on('connection', (socket) => {
  console.log('a user connected');
  socket.on('startRecording', (timestamp) => handleStartRecording(timestamp));
  socket.on('stopRecording', (f) => handleStopRecording());
});



parser.on('data', function(data) {
    const datapoint = parseFloat(data)
    const resistance = (1024+(2*datapoint)) * (1/(512-datapoint))
    const microSiemens = (1/resistance) * 100
    console.log(datapoint, microSiemens, recording)

    let d = {
      conductance: microSiemens,
      timeStamp: Date.now()
    }


    if(recording){
      recordingFile.rows.push(d)
      csv += `${d.conductance},${d.timeStamp}`
      csv += '\n'
    }
    io.emit('data', d);
    
});



server.listen(3000, () => {
  console.log('server running at http://localhost:3000');
});

