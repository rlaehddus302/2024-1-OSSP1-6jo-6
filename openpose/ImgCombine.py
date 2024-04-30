from GetKeypoints import output_keypoints

# 이미지를 불러오고 처리하는 함수 정의
def process_and_load_images(protoFile_mpi, weightsFile_mpi, BODY_PARTS_MPI, image_paths, size=(640, 480)):
    processed_images = []
    for image_path in image_paths:
        frame = cv2.imread(image_path)
        if frame is None:
            print('이미지 로드에 실패했습니다')
            continue
        processed_frame = output_keypoints(frame=frame, proto_file=protoFile_mpi,
                                           weights_file=weightsFile_mpi, threshold=0.2, model_name="MPII", BODY_PARTS=BODY_PARTS_MPI)
        processed_images.append(processed_frame)
    return processed_images

# 이미지들을 동일한 사이즈로 변경
def resize_images(images, size=(480, 480)):
    resized_images = []
    for img in images:
        if img is not None:
            resized = cv2.resize(img, size)
            resized_images.append(resized)
        else:
            print("이미지 로드 실패")
    return resized_images

# 이미지들을 하나의 큰 이미지로 합치는 함수 정의
def combine_images(images, rows, cols):
    # 가로로 합치기
    row_images = []
    for row in range(rows):
        row_images.append(cv2.hconcat(images[row*cols:(row+1)*cols]))
    # 세로로 합치기
    combined_image = cv2.vconcat(row_images)
    return combined_image