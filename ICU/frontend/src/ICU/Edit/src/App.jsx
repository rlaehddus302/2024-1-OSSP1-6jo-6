import reactLogo from './assets/react.svg'
import viteLogo from '/vite.svg'
import Navbar from './Navbar'
import './App.css'
import Table from './Table'
import { useNavigate } from 'react-router-dom'
function App() {
  let navigate = useNavigate();
  function setting_page(){
    navigate('/setting');
  }
  return (
    <>
      <Navbar/>
      <section>
        <div>
          <h1>CCTV 정보</h1>
          <div>
            <Table/>
          </div>
        </div>
        <h1></h1>
      </section>
      <section>
        <div>
          <h1>설정</h1>
          <button style={{backgroundColor:"#5555ee"}} onClick={setting_page}>정보 수정</button>
        </div>
      </section>
    </>
  )
}

export default App
