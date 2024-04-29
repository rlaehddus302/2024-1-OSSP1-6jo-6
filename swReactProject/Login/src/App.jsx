import './App.css'

function App() {

  return (
    <>
      <section className='display'>
        <div className='logIn'>
          <p className='title'>Login</p>
          <p className='main'>아이디와 비밀번호를 입력하세요</p>
          <form>
            <div className='id'>
              <input type="text" id='id' placeholder='아이디' />
            </div>
            <div className='password'>
              <input type="password" id='password' placeholder='비밀번호' />
            </div>
            <button>로그인</button>
            <div>계정이 없으시나요? <a href="">만들기</a></div>
          </form>
        </div>
      </section>
    </>
  )
}

export default App
