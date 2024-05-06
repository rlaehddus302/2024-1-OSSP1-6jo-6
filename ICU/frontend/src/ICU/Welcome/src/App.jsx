import icu from '../public/공개SW 로고.png'
import './App.css'
import Navbar from './Navbar'
function App() {

  return (
    <>
      <div className='welcome'>
        <img className='icu' src={icu} alt="no data" />
        <h1>ICU 프로그램에 오신 것을 환영합니다</h1>
        <p className='main'>ICU는 CCTV 화면과 연동하여 노숙취객 탐지를 제공하는 서비스입니다.</p>
        <button style={{backgroundColor:"#5555ee"}}>로그인</button>
        <button style={{backgroundColor:"#5555ee"}}>회원가입</button>
      </div>
    </>
  )
}

export default App
