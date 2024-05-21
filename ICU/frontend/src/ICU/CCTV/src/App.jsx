import classes from './App4.module.css';
import Navbar from './Navbar';
import { useRef, useState } from 'react';

function App() {
  const [alarm, setAlarm] = useState([{id: 1, camera: 1, message: '기존 알림 메시지'}, {id: 2, camera: 2, message: '기존 알림 메시지'}]);
  const videoRef = useRef(null);
  const fileInputRef = useRef(null);

  function deletion(event, id) {
    const correction = alarm.filter((element) => {
      return (element.id !== id);
    });
    setAlarm(correction);
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
            camera: `1`,
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
            <video ref={videoRef} controls autoPlay>
              <source src='' type='video/mp4' />
            </video>
          </div>
          <ul className={classes.alarm}>
            {alarm.map((element) => {
              return (
                <li key={element.id}>
                  <p>
                    <span className={classes.left}>⚠️ {element.camera}번 카메라 노숙취객 탐지 <span className={classes.subText}>{element.message} 가까운 119 및 112에 신고 요망</span></span>
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
        </div>
      </section>
    </>
  );
}

export default App;
