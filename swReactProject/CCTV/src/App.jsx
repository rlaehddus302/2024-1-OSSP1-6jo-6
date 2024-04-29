import './App.css'
import Navbar from './Navbar'
import Alarm from './Alarm'
import { useRef } from 'react'


function App() {
  const alarm =useRef();
  function Test(event)
  {
    alarm.current.showModal()
  }
  return (
    <>
      <Alarm ref={alarm}/>
      <Navbar/>
      <button onClick={Test}>test</button>
    </>
  )
}

export default App
