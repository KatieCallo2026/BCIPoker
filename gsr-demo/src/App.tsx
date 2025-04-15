import { useState, useEffect } from 'react'
import { LineChart } from '@mui/x-charts'
import { socket } from './socket'
import './App.css'
import { Slider, Typography, Button } from '@mui/material'
import FFT from 'fft.js'

function App() {
  const [xlim, setXLim] = useState(0)
  const [data, setData] = useState<number[]>([])
  const [isConnected, setIsConnected] = useState(socket.connected)
  const [delay, setDelay] = useState(0)
  const [graphInterval, setGraphInterval] = useState(50)
  const [recording, setRecording] = useState(false)
  
  const fftInterval = 32

  const onConnect = () => setIsConnected(true);
  const onDisconnect = () => setIsConnected(false);
  const onData = (d) => {
    const datapoint = d.conductance
    const timestamp = d.timeStamp
    const delay2 = Date.now() - timestamp
    setDelay(delay2)
    let d2 = [...data]
    if(d2.length > graphInterval){
      d2.shift()
    }
    d2.push(parseFloat(datapoint))
    setData(d2)
  }

  useEffect(() => {

    socket.on('connect', onConnect);
    socket.on('disconnect', onDisconnect);
    socket.on('data', onData)
    return () => {
      socket.off('data', onData);
    };
  }, [data])



  const powerSpectrum = (d, size) => {
    if(size > 0 && d.length != 0){
      const f = new FFT(size)
    if (d.length == size){
      const out = f.createComplexArray()
      f.realTransform(out, d)
      const magnitudes = new Array(size / 2);
    for (let j = 0; j < size / 2; j++) {
      magnitudes[j] = Math.sqrt(out[2 * j] ** 2 + out[2 * j + 1] ** 2);
    }

    return magnitudes
    }
      return []
    }
    return []
  }

  const handleRecord = () => {
    
    if(recording){
      socket.emit('stopRecording', Date.now())
    }
    else{
      socket.emit('startRecording', Date.now())
      console.log('emitted')
    }
    setRecording(!recording)
  }

  const handleStreaming = () => {
    if(isConnected){
      socket.disconnect()
    }
    else{
      socket.connect()
    }
  }

  return (
    <>
      <div style={{background: '#FFFFFF', display: 'flex', justifyContent: 'center', alignItems: 'center', flexDirection:'column', height:'100vh', width: '100vw'}}>
          <div style={{display: 'flex', flexDirection: 'row'}}>
         
        <LineChart width={500} height={600} sx={{
          color: '#FFFFFF'
        }}
        series={[{
          data: data.slice(xlim, xlim+graphInterval), 
          showMark: false,
          label: 'GSR in microSiemens (μS)'
        }]} 
        
        xAxis={[{data:data.map((n, i) => i/4).slice(0, graphInterval), label: 'Time in seconds after recording starts'}]}/>
      

        <LineChart width={500} height={600} sx={{
          color: '#FFFFFF'
        }}
        series={[{
          data: powerSpectrum(data.slice(xlim, xlim+fftInterval), fftInterval), 
          showMark: false,
          label: 'Amplitude (GSR in μS)^2 '
        }]}
       xAxis={[{data:data.map((n, i) => i).slice(0, fftInterval), label: 'Frequency in Hz'}]}/>
        </div>
          
          <Slider aria-label="Plotted Interval" value={graphInterval} onChange={(e) => setGraphInterval(e.target.value)} valueLabelDisplay="on" />
          <p style={{color: '#000000'}}>
             ^ Change Interval that is plotted
          </p>
          <Button onClick={handleRecord}>
            {recording ? 'Stop Recording' : 'Start Recording'}
          </Button>

          <Button onClick={handleStreaming}>
            {isConnected ? 'Stop Streaming Data' : 'Start Streaming Data'}
          </Button>
      </div>
    </>
  )
}

export default App
