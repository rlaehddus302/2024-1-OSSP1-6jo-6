import reactLogo from './assets/react.svg'
import viteLogo from '/vite.svg'
import icu from '../public/공개SW 로고.png'
import Navbar from './Navbar'
import './App.css'

function App() {

  return (
    <>
      <Navbar/>
      <section>
        <div className='welcome'>
          <img className='icu' src={icu} alt="no data" />
          <h1>ICU 프로그램에 오신 것을 환영합니다</h1>
          <p className='main'>이 icu 프로그램은 cctv 화면과 연동하여 노숙 취객 탐지를 제공하는 서비스입니다. 
            사람을 자동으로 인식하고 내장된 알고리즘이 움직임이 없다 판단하면 신고 알림을 사용자에게 알려줍니다. </p>
          <button style={{backgroundColor:"#5555ee"}}>로그인</button>
          <button style={{backgroundColor:"#5555ee"}}>회원가입</button>
        </div>
      </section>
    </>
  )
}

export default App
