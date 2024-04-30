def output_keypoints(frame, proto_file, weights_file, threshold, model_name, BODY_PARTS):

  # 네트워크 불러오기
  net = cv2.dnn.readNetFromCaffe(proto_file, weights_file)

  # 입력 이미지의 사이즈 정의
  # 네트워크 효율적 작업을 위해 OpenPose 모델에선 368X368 크기 일반적으로 사용
  image_height = 368
  image_width = 368

  # 네트워크에 넣기 위한 전처리
  # blob : Binary Large Object
  # blob:4차원 배열(이미지수, 채널 수, 높이, 너비)
  input_blob = cv2.dnn.blobFromImage(frame, 1.0 / 255, (image_width, image_height), (0, 0, 0), swapRB=False, crop=False)

  # 네트워크에 전처리된 blob을 입력
  net.setInput(input_blob)

  # 모델이 이미지를 분석하고 결과를 출력
  out = net.forward()
  out_height = out.shape[2]
  out_width = out.shape[3]

  # 원본 이미지의 높이, 너비를 받아오기
  frame_height, frame_width = frame.shape[:2]

  # 포인트 리스트 초기화
  points = []

  #print(f"\n============================== {model_name} Model ==============================")
  for i in range(len(BODY_PARTS)):

    # 신체 부위의 confidence map
    prob_map = out[0, i, :, :]

    # 최소값, 최대값, 최소값 위치, 최대값 위치
    min_val, prob, min_loc, point = cv2.minMaxLoc(prob_map)

    # 원본 이미지에 맞게 포인트 위치 조정
    x = (frame_width * point[0]) / out_width
    x = int(x)
    y = (frame_height * point[1]) / out_height
    y = int(y)

    if prob > threshold: #[pointed]
      cv2.circle(frame, (x,y), 5, (0, 255, 255), thickness=-1, lineType=cv2.FILLED)
      cv2.putText(frame, str(i), (x, y), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 0, 255), 1, lineType=cv2.LINE_AA)

      points.append((x,y))
      #print(f"[pointed] {BODY_PARTS[i]} ({i}) => prob: {prob:.5f} / x: {x} / y: {y}")

    else: #[not pointed]
      cv2.circle(frame, (x, y), 5, (0, 255, 255), thickness=-1, lineType=cv2.FILLED)
      cv2.putText(frame, str(i), (x,y), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 0, 0), 1, lineType=cv2.LINE_AA)

      points.append(None)
      #print(f"[not pointed] {BODY_PARTS[i]} ({i}) => prob: {prob:.5f} / x: {x} / y: {y}")

  #cv2_imshow(frame)
  #cv2.waitKey(0)
  return frame