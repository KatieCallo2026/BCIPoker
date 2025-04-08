import express from 'express';
import { createServer } from 'node:http';
import { SerialPort, ReadlineParser } from 'serialport';
import { Server } from 'socket.io';
import cors from 'cors'

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

io.on('connection', (socket) => {
    console.log('a user connected');
  });


let recording = false

io.on('record', (f) => {
  recording = true
})

io.off('record', (f) => {
  if(recording == true){
    
  }
  recording = false
})

parser.on('data', function(data) {
    const datapoint = parseFloat(data)
    const resistance = (1024+(2*datapoint)) * (1/(512-datapoint))
    const microSiemens = (1/resistance) * 100
    console.log(datapoint, microSiemens)
    io.emit('data', microSiemens);
    
});



server.listen(3000, () => {
  console.log('server running at http://localhost:3000');
});

