import cv2
import mediapipe as mp
import numpy as np
import os

# 미디어파이프 솔루션 초기화
mp_pose = mp.solutions.pose
pose = mp_pose.Pose(static_image_mode=True, min_detection_confidence=0.5)
mp_drawing = mp.solutions.drawing_utils

# 이미지 파일 경로
image_dir = 'C:/picture'
input_image_path = os.path.join(image_dir, '15.jpg')
output_image_path = os.path.join(image_dir, '15_pose_output.jpg')

# 각 관절 포인트의 이름 정의
keypoint_names = [
    "Nose", "Left Eye", "Right Eye", "Left Ear", "Right Ear",
    "Left Shoulder", "Right Shoulder", "Left Elbow", "Right Elbow",
    "Left Wrist", "Right Wrist", "Left Hip", "Right Hip",
    "Left Knee", "Right Knee", "Left Ankle", "Right Ankle"
]

def get_keypoint(landmarks, index):
    """ keypoints 리스트에서 특정 index의 keypoint 좌표를 반환 """
    return landmarks.landmark[index].x, landmarks.landmark[index].y, landmarks.landmark[index].visibility

def classify_pose(landmarks):
    """ keypoints 정보를 기반으로 자세를 분류 """
    left_shoulder_x, left_shoulder_y, left_shoulder_conf = get_keypoint(landmarks, mp_pose.PoseLandmark.LEFT_SHOULDER)
    right_shoulder_x, right_shoulder_y, right_shoulder_conf = get_keypoint(landmarks, mp_pose.PoseLandmark.RIGHT_SHOULDER)
    left_hip_x, left_hip_y, left_hip_conf = get_keypoint(landmarks, mp_pose.PoseLandmark.LEFT_HIP)
    right_hip_x, right_hip_y, right_hip_conf = get_keypoint(landmarks, mp_pose.PoseLandmark.RIGHT_HIP)
    left_knee_x, left_knee_y, left_knee_conf = get_keypoint(landmarks, mp_pose.PoseLandmark.LEFT_KNEE)
    right_knee_x, right_knee_y, right_knee_conf = get_keypoint(landmarks, mp_pose.PoseLandmark.RIGHT_KNEE)

    if (left_shoulder_conf > 0.5 and right_shoulder_conf > 0.5 and
        left_hip_conf > 0.5 and right_hip_conf > 0.5 and
        (left_knee_conf > 0.5 or right_knee_conf > 0.5)):

        left_side_sorted = left_shoulder_y < left_hip_y < left_knee_y if left_knee_conf > 0.5 else False
        right_side_sorted = right_shoulder_y < right_hip_y < right_knee_y if right_knee_conf > 0.5 else False

        if left_knee_conf > 0.5 and right_knee_conf > 0.5:
            mid_knee_x = (left_knee_x + right_knee_x) / 2
            mid_knee_y = (left_knee_y + right_knee_y) / 2
        elif left_knee_conf > 0.5:
            mid_knee_x = left_knee_x
            mid_knee_y = left_knee_y
        else:
            mid_knee_x = right_knee_x
            mid_knee_y = right_knee_y

        mid_shoulder_x = (left_shoulder_x + right_shoulder_x) / 2
        mid_shoulder_y = (left_shoulder_y + right_shoulder_y) / 2
        x_diff = abs(mid_shoulder_x - mid_knee_x)
        y_diff = abs(mid_shoulder_y - mid_knee_y)

        if (left_side_sorted or right_side_sorted) and x_diff < y_diff:
            return "Standing"
        
    return "Not Standing"

def add_text(image, text, position, color):
    """ 이미지에 텍스트를 추가 """
    cv2.putText(image, text, position, cv2.FONT_HERSHEY_SIMPLEX, 1.5, color, 3)

# 이미지 읽기
image = cv2.imread(input_image_path)
if image is None:
    print(f"이미지를 읽을 수 없습니다: {input_image_path}")
else:
    # 이미지가 BGR 형식이므로 RGB로 변환
    image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    
    # 포즈 추정 수행
    results = pose.process(image_rgb)
    
    # 포즈 랜드마크 그리기
    if results.pose_landmarks:
        # 포즈 랜드마크를 복사하여 원본 이미지를 변경하지 않도록 함
        annotated_image = image.copy()
        mp_drawing.draw_landmarks(
            annotated_image, results.pose_landmarks, mp_pose.POSE_CONNECTIONS)
        
        # 자세 분류 및 텍스트 표시
        pose_classification = classify_pose(results.pose_landmarks)
        text_position = (50, 50)  # 텍스트 표시 위치
        add_text(annotated_image, pose_classification, text_position, (0, 255, 255))  # 노란색

        # 서 있지 않으면 경고 메시지 추가
        if pose_classification == "Not Standing":
            box = results.pose_landmarks.landmark[mp_pose.PoseLandmark.LEFT_HIP]
            x, y = int(box.x * image.shape[1]), int(box.y * image.shape[0])
            add_text(annotated_image, "Warning", (x, y + 30), (0, 0, 255))  # 빨간색

        # 결과 이미지 저장
        cv2.imwrite(output_image_path, annotated_image)
        print(f"결과 이미지를 '{output_image_path}'에 저장했습니다.")
        
        # 결과 이미지 표시
        cv2.imshow('MediaPipe Pose', annotated_image)
    else:
        print("포즈 랜드마크를 감지하지 못했습니다.")
    
    cv2.waitKey(0)
    cv2.destroyAllWindows()
