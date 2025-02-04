import { useState, useEffect } from 'react'
import { LineChart } from '@mui/x-charts'
import { useInterval } from 'usehooks-ts'
import './App.css'
import { Slider, Typography } from '@mui/material'
import FFT from 'fft.js'

function App() {
  const [xlim, setXLim] = useState(0)
  const [data, setData] = useState([])
  const [graphInterval, setGraphInterval] = useState(50)
  
  const fftInterval = 32

  useEffect(() => {
      fetch( './EDA.csv' )
          .then( response => response.text() )
          .then( responseText => {
              console.log(responseText)
              const signal = responseText.split("\n")
              const num_signal = signal.map((n) => parseFloat(n)).slice(2)
              setData(num_signal)
          })

  }, [])

  useInterval(() => {
    if(xlim + 1 > data.length){
      setXLim(0)
    }
    setXLim(xlim + 1)
  }, 20)

  const powerSpectrum = (d, size) => {
    if(size > 0 && d.length != 0){
      console.log('here')
      const f = new FFT(size)
    if (d.length == size){
      console.log('here2')
      const out = f.createComplexArray()
      f.realTransform(out, d)
      const magnitudes = new Array(size / 2);
    for (let j = 0; j < size / 2; j++) {
      magnitudes[j] = Math.sqrt(out[2 * j] ** 2 + out[2 * j + 1] ** 2);
    }
    console.log(magnitudes)

    return magnitudes
    }
      return []
    }
    return []
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
      </div>
    </>
  )
}

export default App
