import torch
import cv2
import os
import sys

# YOLOv5 모델 로드
#sys.path.insert(0, './2024-1-OSSP1-6jo-6/ICU_YOLO')
model = torch.hub.load('./backend/yolov5','custom',path='./backend/yolov5/best.pt',source='local', force_reload=True)

def detect_people(image):
    results = model(image)
    people_coords = []
    for result in results.xyxy[0].cpu().numpy():
        if int(result[5]) == 0:  # 클래스 0은 '사람'을 의미
            x1, y1, x2, y2 = result[:4]
            people_coords.append((x1, y1, x2, y2))
    return people_coords

def calculate_center(coord):
    x1, y1, x2, y2 = coord
    center_x = (x1 + x2) / 2
    center_y = (y1 + y2) / 2
    return (center_x, center_y)

def is_stationary(coord1, coord2, threshold=0.25):
    center1 = calculate_center(coord1)
    center2 = calculate_center(coord2)

    width1, height1 = coord1[2] - coord1[0], coord1[3] - coord1[1]

    dx = abs(center1[0] - center2[0])
    dy = abs(center1[1] - center2[1])

    if dx <= threshold * width1 and dy <= threshold * height1:
        return True
    return False

def track_people_from_video(video_path, output_set):
    cap = cv2.VideoCapture(video_path)
    fps = cap.get(cv2.CAP_PROP_FPS)
    frame_interval = int(fps)  # 1초마다 프레임 추출

    tracked_people = []
    output_index = 1

    frame_count = 0
    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break

        if frame_count % frame_interval == 0:
            current_frame_people = detect_people(frame)

            centers = [calculate_center(coord) for coord in current_frame_people]
            print(f"Number of people: {len(current_frame_people)}")
            for j, center in enumerate(centers):
                print(f"Person {j + 1} center: {center}")

            if frame_count == 0:
                tracked_people = [[(coord, 1)] for coord in current_frame_people]
            else:
                for coord in current_frame_people:
                    matched = False
                    for tracked in tracked_people:
                        if is_stationary(tracked[-1][0], coord):
                            tracked.append((coord, tracked[-1][1] + 1))
                            matched = True
                            break
                    if not matched:
                        tracked_people.append([(coord, 1)])
            new_tracked_people = []
            for person in tracked_people:
                if len(person) >= 10 and person[-1][1] >= 7:
                    stationary_people_coord = person[-1][0]
                    alert_message = "Detected stationary person!"
                else:
                    new_tracked_people.append(person)
            tracked_people = new_tracked_people
        
        frame_count += 1

    cap.release()
    cv2.destroyAllWindows()
    return alert_message

def draw_boxes(image, people_coords):
    for coord in people_coords:
        x1, y1, x2, y2 = map(int, coord)
        cv2.rectangle(image, (x1, y1), (x2, y2), (0, 255, 0), 2)
        cv2.putText(image, "Detected People!", (x1, y1 - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (0, 255, 0), 2)
    return image