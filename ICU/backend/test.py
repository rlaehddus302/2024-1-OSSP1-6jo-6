import pathlib
temp = pathlib.PosixPath
pathlib.PosixPath = pathlib.WindowsPath

import torch
import cv2
import mediapipe as mp
import numpy as np
import sys

# YOLOv5 모델 로드
model = torch.hub.load('./backend/yolov5', 'custom', path='./backend/yolov5/best.pt', source='local', force_reload=True)

mp_pose = mp.solutions.pose
pose = mp_pose.Pose(static_image_mode=True, min_detection_confidence=0.5)
mp_drawing = mp.solutions.drawing_utils
keypoint_names = [
    "Nose", "Left Eye", "Right Eye", "Left Ear", "Right Ear",
    "Left Shoulder", "Right Shoulder", "Left Elbow", "Right Elbow",
    "Left Wrist", "Right Wrist", "Left Hip", "Right Hip",
    "Left Knee", "Right Knee", "Left Ankle", "Right Ankle"
]

def mid_coordinate(left, right):
    if left[2] > 0.5 and right[2] > 0.5:
        mid_x = (left[0] + right[0]) / 2
        mid_y = (left[1] + right[1]) / 2
    elif left[2] > 0.5:
        mid_x = left[0]
        mid_y = left[1]
    else:
        mid_x = right[0]
        mid_y = right[1]
    return mid_x, mid_y

def get_keypoint(landmarks, index):
    """ keypoints 리스트에서 특정 index의 keypoint 좌표를 반환 """
    return landmarks.landmark[index].x, landmarks.landmark[index].y, landmarks.landmark[index].visibility

def calculate_angle(a, b, c):
    """ a, b, c 좌표를 받아서 벡터 간의 각도를 계산 """
    a = np.array(a)
    b = np.array(b)
    c = np.array(c)
    
    ab = a - b
    cb = c - b
    
    dot_product = np.dot(ab, cb)
    ab_magnitude = np.linalg.norm(ab)
    cb_magnitude = np.linalg.norm(cb)
    
    cos_theta = dot_product / (ab_magnitude * cb_magnitude)
    angle = np.arccos(cos_theta)
    
    return np.degrees(angle)

def detect_people(image):
    results = model(image)
    people_coords = []
    for result in results.xyxy[0].cpu().numpy():
        if int(result[5]) == 0:  # 클래스 0은 '사람'을 의미
            x1, y1, x2, y2 = result[:4]
            people_coords.append((x1, y1, x2, y2))
    return people_coords

def classify_pose(landmarks):
    """ keypoints 정보를 기반으로 자세를 분류 """
    left_shoulder = get_keypoint(landmarks, mp_pose.PoseLandmark.LEFT_SHOULDER)
    right_shoulder = get_keypoint(landmarks, mp_pose.PoseLandmark.RIGHT_SHOULDER)
    left_hip = get_keypoint(landmarks, mp_pose.PoseLandmark.LEFT_HIP)
    right_hip = get_keypoint(landmarks, mp_pose.PoseLandmark.RIGHT_HIP)
    left_knee = get_keypoint(landmarks, mp_pose.PoseLandmark.LEFT_KNEE)
    right_knee = get_keypoint(landmarks, mp_pose.PoseLandmark.RIGHT_KNEE)
    left_eye = get_keypoint(landmarks, mp_pose.PoseLandmark.LEFT_EYE)
    right_eye = get_keypoint(landmarks, mp_pose.PoseLandmark.RIGHT_EYE)
    left_ankle = get_keypoint(landmarks, mp_pose.PoseLandmark.LEFT_ANKLE)
    right_ankle = get_keypoint(landmarks, mp_pose.PoseLandmark.RIGHT_ANKLE)
    
    if (left_shoulder[2] > 0.5 and right_shoulder[2] > 0.5 and
        left_hip[2] > 0.5 and right_hip[2] > 0.5 and
        (left_knee[2] > 0.5 or right_knee[2] > 0.5)):

        left_side_sorted = left_shoulder[1] < left_hip[1] < left_knee[1] if left_knee[2] > 0.5 else False
        right_side_sorted = right_shoulder[1] < right_hip[1] < right_knee[1] if right_knee[2] > 0.5 else False

        mid_knee_x, mid_knee_y = mid_coordinate(left_knee, right_knee)
        mid_shoulder_x, mid_shoulder_y = mid_coordinate(left_shoulder, right_shoulder)
        mid_hip_x, mid_hip_y = mid_coordinate(left_hip, right_hip)
        x_diff = abs(mid_shoulder_x - mid_knee_x)
        y_diff = abs(mid_shoulder_y - mid_knee_y)
        
 # Extract the x and y coordinates
        eye_mid_y = mid_coordinate(left_eye, right_eye)[1]
        left_ankle_x, left_ankle_y = left_ankle[:2]
        right_ankle_x, right_ankle_y = right_ankle[:2]

        # Calculate min and max x and y values
        x_values = [left_ankle_x, right_ankle_x, mid_coordinate(left_eye, right_eye)[0]]
        y_values = [left_ankle_y, right_ankle_y, eye_mid_y]

        x_min, x_max = min(x_values), max(x_values)
        y_min, y_max = min(y_values), max(y_values)

        # Calculate box_ratio
        box_ratio = (y_max - y_min) / (x_max - x_min)
                
        angle = calculate_angle((mid_shoulder_x, mid_shoulder_y), (mid_hip_x, mid_hip_y), (mid_knee_x, mid_knee_y))
        if (left_side_sorted or right_side_sorted) and 2 * x_diff < y_diff and angle > 120:
            return "Standing"
        elif box_ratio >= 3:
            return "Standing"
    return "Not Standing"

def get_landmark(image):
    image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    
    # 포즈 추정 수행
    results = pose.process(image_rgb)
    
    # 포즈 랜드마크 그리기
    if results.pose_landmarks:
        # 포즈 랜드마크를 복사하여 원본 이미지를 변경하지 않도록 함
        annotated_image = image.copy()
        mp_drawing.draw_landmarks(
            annotated_image, results.pose_landmarks, mp_pose.POSE_CONNECTIONS)
        
    #     # 자세 분류 및 텍스트 표시
    #     pose_classification = classify_pose(results.pose_landmarks)
    # return pose_classification
    return classify_pose(results.pose_landmarks)

def calculate_center(coord):
    x1, y1, x2, y2 = coord
    center_x = (x1 + x2) / 2
    center_y = (y1 + y2) / 2
    return center_x, center_y

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
    alert_message = None

    pose_classification = ''

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
                    try:
                        x1, y1, x2, y2 = map(int, stationary_people_coord)
                        person_image = frame[y1:y2, x1:x2]
                        pose_classification = get_landmark(person_image)
                        if pose_classification == "Not Standing":
                            alert_message = "Detected stationary person!"
                    except Exception as e:
                        print(e)
                else:
                    new_tracked_people.append(person)
            tracked_people = new_tracked_people
        
        frame_count += 1

    cap.release()
    cv2.destroyAllWindows()
    return alert_message


def draw_boxes(image, coords, color=(0, 255, 0), thickness=2):
    for (x1, y1, x2, y2) in coords:
        cv2.rectangle(image, (int(x1), int(y1)), (int(x2), int(y2)), color, thickness)
    return image