import { forwardRef } from "react"

const Alarm = forwardRef(function(prop,ref){
    return(
        <dialog ref={ref}>
            <form method="dialog">
                <h2>카메라가 탐지했습니다</h2>
                <div>112나 119에 신고하세요</div>
                <button>확인</button>
            </form>
        </dialog>
    )
})

export default Alarm;