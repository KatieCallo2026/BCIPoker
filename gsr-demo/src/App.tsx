import { useState, useEffect } from 'react'
import reactLogo from './assets/react.svg'
import viteLogo from '/vite.svg'
import { LineChart } from '@mui/x-charts'
import { useInterval } from 'usehooks-ts'
import './App.css'
import { Slider, Typography } from '@mui/material'

function App() {
  const [xlim, setXLim] = useState(0)
  const [data, setData] = useState([])
  const [graphInterval, setGraphInterval] = useState(50)
 
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

  return (
    <>
      <div style={{background: '#FFFFFF'}}>
        <LineChart width={1000} height={600} sx={{
          color: '#FFFFFF'
        }}
        series={[{
          data: data.slice(xlim, xlim+graphInterval), 
          showMark: false,
          label: 'GSR in microSiemens (μS)'
        }]} 
          xAxis={[{data:data.map((n, i) => i/4).slice(0, graphInterval), label: 'Time in seconds after recording starts'}]}/>
          <Slider aria-label="Plotted Interval" value={graphInterval} onChange={(e) => setGraphInterval(e.target.value)} valueLabelDisplay="on" />
          <p style={{color: '#000000'}}>
             ^ Change Interval that is plotted
          </p>
      </div>
    </>
  )
}

export default App
