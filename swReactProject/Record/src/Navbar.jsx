import icu from '../public/공개SW 로고.png'

export default function Navbar()
{
    return(
        <ul className='navBar'>
            <li className='photo'>
                <img src={icu} alt="no data" />
            </li>
            <li className='icu'>
                <div>ICU</div>
            </li>
            <li>
                <a href="">cctv 화면</a>
            </li>
            <li>
                <a href="">기록</a>
            </li>
            <li>
                <a href="">메인</a>
            </li>
        </ul>
    )
}