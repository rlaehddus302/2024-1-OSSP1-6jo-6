import classes from './App4.module.css'
import Navbar from './Navbar'
import { useRef } from 'react'
import { useState, useEffect } from 'react'
import Cookies from 'js-cookie'

function App() {
  const [alarm, setAlarm] = useState([{id: 1, camera: 1, message: '기존 알림 메시지'}, {id: 2, camera: 2, message: '기존 알림 메시지'}]);
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
        photoUpload(data)
      const intervalId = setInterval(() => {
          photoUpload(data)
        }, 50000);
      return () => clearInterval(intervalId);
    }, []);
  function deletion(event,id)
  {
    const correction=alarm.filter((element)=>{
      return(element.id != id)
    })
    console.log(correction)
    setAlarm(correction)
  }

  async function photoUpload(data) {
    console.log(data[0].ip , data[0].port)
    const data1= {"ip": data[0].ip, "port": data[0].port}
    try {
      const response = await fetch('http://localhost:8000/upload_video/',{ 
      method : 'POST',
      headers : {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify(data1),
    });
      const data = await response.json();
      if (response.ok) {
        if (data.message) {
          setAlarm((currentAlarms) => {
            console.log(currentAlarms.length)
            const newAlarm = {
              id: currentAlarms.length + 1,
              camera: "1",
              message: data.message
            };
            return [...currentAlarms, newAlarm];
          });
        } else {
          alert('Success: File uploaded successfully!');
        }
      } else {
        alert('Error: File upload failed.');
      }
    } catch (error) {
      console.error('Error:', error);
      alert('Error: An error occurred while uploading the file.');
    }
  }

  async function VideoFileChange(event) {
    const file = event.target.files[0];
    const url = URL.createObjectURL(file);
    videoRef.current.src = url;

    // 비디오 파일을 Django로 전송
    const formData = new FormData();
    formData.append('video', file);

    try {
      const response = await fetch('http://localhost:8000/upload_video/', {  // Django 서버의 URL
        method: 'POST',
        body: formData,
      });
      const data = await response.json();
      if (response.ok) {
        if (data.message) {
          // 새로운 알림 추가
          const newAlarm = {
            id: alarm.length + 1,
            camera: "1",
            message: data.message
          };
          setAlarm([...alarm, newAlarm]);
        } else {
          alert('Success: File uploaded successfully!');
        }
      } else {
        alert('Error: File upload failed.');
      }
    } catch (error) {
      console.error('Error:', error);
      alert('Error: An error occurred while uploading the file.');
    }
  }
  
  return (
    <>
      <Navbar />
      <section className={classes.section}>
        <div>
          <div>
            <h3>Live Video Stream</h3>
            <ul className={classes.cctv}>
              {content.map((item, index)=>{ return(
                <li key={index+1}>
                  <img ref={videoRef} src={`https://${item.ip}:${item.port}/video`} alt="not find" />
                </li>
              )})}
            </ul>
          </div>
          <ul className={classes.alarm}>
            {alarm.map((element) => {
              return (
                <li key={element.id}>
                  <p>
                    <span className={classes.left}>⚠️ {element.camera}번 카메라 <span className={classes.subText}>{element.message} 즉시 신고 요망</span></span>
                    <span onClick={(event) => deletion(event, element.id)} className={classes.right}>❌</span>
                  </p>
                </li>
              );
            })}
          </ul>
          <div>
            <h3>Load Video File</h3>
            <input
              type='file'
              ref={fileInputRef}
              accept='video/*'
              onChange={VideoFileChange}
            />
          </div>
          <button onClick={photoUpload}>전송</button>
        </div>
      </section>
    </>
  );
}

export default App;
