import axios from 'axios'
import classes from './App3.module.css'

function Submit(event) {
  event.preventDefault();
  const UserData={
    id:document.getElementById('id').value,
    password:document.getElementById('password').value
  };
  axios.post('http://localhost:8000/login',UserData)
  .then(response =>{
    console.log('Token:',response.data);
    alert("로그인 성공");
  })
  .catch(error =>console.error('Login error:',error));
  alert("로그인 실패");
}

axios.interceptors.request.use(
  config =>{
    const token = localStorage.getItem('accessToken');
    if(token){
      config.headers['Authorization'] = 'Bearer '+token;
    }
    return config;
  },
  error =>{
    return Promise.reject(error);
  }
);
axios.interceptors.response.use(
  response => response,
  error =>{
    if(error.response && error.response.status === 401){
      localStorage.removeItem('accessToken');
      window.location = '/login'
    }
    return Promise.reject(error);
  }
);





function App() {

  return (
    <>
      <section className={classes.display}>
        <div className={classes.logIn}>
          <p className={classes.title}>Login</p>
          <p className='main'>아이디와 비밀번호를 입력하세요</p>
          <form onSubmit={Submit}>
            <div className={classes.id}>
              <input type="text" id='id' placeholder='아이디' />
            </div>
            <div className={classes.password}>
              <input type="password" id='password' placeholder='비밀번호' />
            </div>
            <button type = 'submit'>로그인</button>
            <div>계정이 없으신가요? <a href="signup">만들기</a></div>
          </form>
        </div>
      </section>
    </>
  )
}

export default App
