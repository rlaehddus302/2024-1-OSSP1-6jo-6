import cv2
import torch
import time
import pathlib
from PIL import Image, ImageDraw
import numpy as np
import tkinter as tk
from tkinter import messagebox

def show_alert():
    root = tk.Tk()
    root.withdraw()  
    messagebox.showwarning("알림", "사람이 멈춰있습니다.")
    root.destroy()  
temp = pathlib.PosixPath
pathlib.PosixPath = pathlib.WindowsPath

def boxes_overlap(boxA, boxB):
    # 두 박스가 겹치는지 확인 (교차 영역의 면적이 0보다 큰지 확인)
    xA = max(boxA[0], boxB[0])
    yA = max(boxA[1], boxB[1])
    xB = min(boxA[2], boxB[2])
    yB = min(boxA[3], boxB[3])

    # 겹치는 영역이 존재하는지 확인
    overlap = max(0, xB - xA + 1) * max(0, yB - yA + 1) > 0
    return overlap

# 모델 불러오기

model = torch.hub.load('ultralytics/yolov5', 'custom', path='C:/Users/gky03/OneDrive/바탕 화면/icu/icu_yolo.pt')

# 캠 설정
cap = cv2.VideoCapture(0)

start_time = time.time()
capture_interval = 1  # 간격
detection_count = 0
alert_threshold = 5  # 알림을 보낼 탐지 횟수의 임계값
prev_boxes = []  # 이전에 탐지된 바운딩 박스를 저장할 리스트


# 메인 루프 내에서 이전에 사용된 iou 기반의 검사 대신 boxes_overlap 함수를 사용
try:
    while True:
        ret, frame = cap.read()
        current_time = time.time()

        if ret:
            if current_time - start_time >= capture_interval:
                start_time = current_time
                
                img = Image.fromarray(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))
                results = model(img)

                current_boxes = []
                for *xyxy, conf, cls in results.xyxy[0]:
                    current_boxes.append([int(xyxy[0]), int(xyxy[1]), int(xyxy[2]), int(xyxy[3])])

                if prev_boxes:
                    match_found = False
                    for prev_box in prev_boxes:
                        for curr_box in current_boxes:
                            if boxes_overlap(prev_box, curr_box):  # 여기서 검사를 다르게 처리
                                match_found = True
                                break
                        if match_found:
                            break
                    
                    if match_found:
                        detection_count += 1
                    else:
                        detection_count = 0

                    if detection_count > alert_threshold:
                        draw = ImageDraw.Draw(img)
                        for box in current_boxes:
                            draw.rectangle(((box[0], box[1]), (box[2], box[3])), outline="red", width=2)
                        img.save("C:/Users/gky03/OneDrive/바탕 화면/PDF/detected_person.png")  # 저장할 파일 이름과 경로
                        show_alert()
                        detection_count = 0
                
                prev_boxes = current_boxes

            cv2.imshow('frame', frame)

            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
        else:
            break
finally:
    cap.release()
    cv2.destroyAllWindows()

