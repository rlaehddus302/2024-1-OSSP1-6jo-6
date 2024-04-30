#openpose 구동에 필요한 모듈 임포트
#from google.colab.patches import cv2_imshow
from ImgCombine import *
import sys
import numpy as np
import cv2

BODY_PARTS_MPI = {0: "Head", 1: "Neck", 2: "RShoulder", 3: "RElbow", 4: "RWrist",
                  5: "LShoulder", 6: "LElbow", 7: "LWrist", 8: "RHip", 9: "RKnee",
                  10: "RAnkle", 11: "LHip", 12: "LKnee", 13: "LAnkle", 14: "Chest",
                  15: "Background"}

POSE_PAIRS_MPI = [[0,1], [1, 2], [1, 5], [1, 14], [2, 3], [3, 4], [5, 6],
                   [6, 7], [8, 9],[9, 10], [11, 12], [12, 13], [14, 8], [14, 11]]

# 신경 네트워크의 구조를 지정하는 prototxt 파일 (다양한 계층이 배열되는 방법 등)
protoFile_mpi = "set_dir_for_prototxt"
# 훈련된 모델의 weight를 저장하는 caffemodel 파일
weightsFile_mpi = f"set_dir_for_caffemodel"



# 이미지 경로 리스트
image_list = ["./1/100.png", "./1/101.png", "./1/102.png", "./1/103.png",
              "./1/104.png", "./1/105.png", "./1/106.png", "./1/107.png"]

# 이미지 처리
processed_images = process_and_load_images(image_list)

# 이미지 크기 조정
resized_images = resize_images(processed_images, size=(368, 368))

# 4행 2열로 이미지 합치기
combined_image = combine_images(resized_images, 4, 2)

# 합쳐진 이미지 보여주기
#cv2_imshow(combined_image) #코랩버전
cv2.imshow(combined_image)
cv2.waitKey(0)
cv2.destroyAllWindows()
