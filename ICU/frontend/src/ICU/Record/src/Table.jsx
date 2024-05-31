import { useState,useEffect } from "react"
import classes from './Table.module.css'

export default function Table()
{
    const [content,setContent]=useState([])
    function deletion(id)
    {
        const temp = content.filter((element)=>{
            return(
                element.id != id
            )
        })
        setContent(temp)
        getDelete(id)
    }
    async function getDelete(id) 
    {
        try {
            const response = await fetch('http://localhost:8000/test/',{ 
            method : 'DELETE',
            headers : {
              'Content-Type': 'application/json',
            },
            body: JSON.stringify(id),
          });
        }
        catch (error) 
        {
          console.error('Error:', error);
          alert('Error: An error occurred while getting the data.');
        }
    }
    async function getData() 
    {
        try 
        {
          const response = await fetch('http://localhost:8000/test/')
          const data = await response.json();
          if (response.ok) 
            {
                setContent((currentContent) => 
                {
                  return [...data.timeList];
                });
               
            }
        } 
        catch (error) 
        {
          console.error('Error:', error);
          alert('Error: An error occurred while getting the data.');
        }
    }
      useEffect(() => 
        {
            getData()
        }, []);
    return(
        <>
            <table className={classes.table}>
                <thead>
                    <tr>
                        <th scope="col">카메라</th>
                        <th scope="col">날짜</th>
                        <th scope="col">시간</th>
                        <th scope="col">삭제</th>
                    </tr>
                 </thead>
                 <tbody>
                    {content.map((element)=>
                    {
                        return(
                            <tr key={element.id}>
                                <td>{element.camera}</td>
                                <td>{element.day}</td>
                                <td>{element.time}</td>
                                <td><button onClick={()=>deletion(element.id)}>삭제</button></td>
                            </tr>
                        )
                    })}
                </tbody>  
            </table>
        </>
    )
}