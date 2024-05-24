import classes from './App4.module.css'
import Navbar from './Navbar'
import { useRef } from 'react'
import { useState, useEffect } from 'react'
import Cookies from 'js-cookie'

function App() {
  const [alarm,setAlarm]=useState([{id : 1, camera : 1},{id : 2, camera : 2}]);
  const videoRef = useRef(null);
  const fileInputRef = useRef(null);
  const [content, setContent] = useState([]);

  useEffect(() => 
    {
      let data = JSON.parse(Cookies.get("IPandPORT") || "[]");
      if (data.length > 0 && !data[0].id) 
        {
          data = data.map((item, index) => ({ ...item, id: index + 1 }));
          Cookies.set('IPandPORT', JSON.stringify(data));  // 쿠키 업데이트
        }
        setContent(data);
    }, []);
  function deletion(event,id)
  {
    const correction=alarm.filter((element)=>{
      return(element.id != id)
    })
    console.log(correction)
    setAlarm(correction)
  }
  
  function VideoFileChange(event){
    const file = event.target.files[0];
    const url = URL.createObjectURL(file);
    videoRef.current.src = url;
  }
  return (
    <>
      <Navbar/>
      <section className={classes.section}>
        <div>
          <div>
            <h3>Live Video Stream</h3>
            <ul className={classes.cctv}>
              {content.map((item, index)=>{ return(
                <li key={index+1}>
                  <video ref={videoRef} controls autoPlay>
                    <source src='' type='video/mp4'/>
                  </video>
                </li>
              )})}
            </ul>
          </div>
          <ul className={classes.alarm}>
            {alarm.map((element)=>{
              return (
              <li key={element.id}>
                <p><span className={classes.left}>⚠️{element.camera}번 카메라 노숙취객 탐지 <span className={classes.subText}> 가까운 119 및 112에 신고 요망</span></span><span onClick={() => deletion(event,element.id)} className={classes.right}>❌</span></p>
              </li>)})}
          </ul>
          <div>
            <h3>Load Video File</h3>
            <input
              type='file'
              ref = {fileInputRef}
              accept='video/*'
              onChange={VideoFileChange}
            />
          </div>
        </div>
      </section>
    </>
  )
}

export default App
