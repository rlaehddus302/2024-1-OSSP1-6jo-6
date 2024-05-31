import os
from django.conf import settings
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.core.files.storage import default_storage
from django.core.files.base import ContentFile
from .test import track_people_from_video  # 함수가 있는 파일에서 가져오기
from django.views.decorators.http import require_http_methods
import subprocess
import json
from datetime import datetime
import pytz


value = {"timeList" : [{"id":1, "camera": "1", "day": "2024-05-05", "time": "12:00:01"},
    {"id":2, "camera": "1", "day": "2024-05-05", "time": "13:00:01"}]}

def save_rtsp_stream(rtsp_url, output_file):
    command = [
        'ffmpeg',
        '-y', #기존 파일 덮어쓰기
        '-i', rtsp_url,  # RTSP 스트림 주소
        '-c', 'copy',  # 오디오와 비디오를 재인코딩하지 않음
        '-t', '30',  # 영상의 길이를 30초로 제한
        output_file  # 저장할 파일 경로
    ]
    try:
        subprocess.run(command, check=True)
    except subprocess.CalledProcessError as e:
        print(f"Error saving RTSP stream: {e}")

@csrf_exempt
def upload_and_process_video(request):
    if request.method == 'POST' and request.FILES.get('video'):
        video_file = request.FILES['video']
        file_name = default_storage.save(video_file.name, ContentFile(video_file.read()))
        file_path = os.path.join(settings.MEDIA_ROOT, file_name)

        # 비디오 파일을 처리
        output_set = os.path.join(settings.MEDIA_ROOT, 'output')
        if not os.path.exists(output_set):
            os.makedirs(output_set)

        alert_message = track_people_from_video(file_path, output_set)
        
        track_people_from_video(file_path, output_set)

        return JsonResponse({'message': alert_message})
    if request.method == 'POST':
        data = json.loads(request.body)
        ip = data.get('ip')
        port = data.get('port')
        save_rtsp_stream("rtsp://"+str(ip)+":"+str(port)+"/h264.sdp",'../video.mp4')
        output_set = os.path.join(settings.MEDIA_ROOT, 'output')
        if not os.path.exists(output_set):
            os.makedirs(output_set)
        alert_message = track_people_from_video('../video.mp4', output_set)
        if alert_message == "취객 감지":
            timezone = pytz.timezone('Asia/Seoul')
            value["timeList"].append({"id" : len(value["timeList"])+1,
                                      "camera": "1", 
                                      "day" : str(datetime.now(timezone).date()),
                                      "time" : datetime.now(timezone).strftime("%H:%M:%S"),
                                      })
        return JsonResponse({'message': alert_message})
    return JsonResponse({'error': 'Invalid request'}, status=400)

@csrf_exempt
def test_upload_image(request):
    if request.method == 'GET':
        return JsonResponse(value)
    if request.method == 'DELETE':
        data = json.loads(request.body)
        value["timeList"] = [x for x in value["timeList"] if x["id"] != data]
        return JsonResponse(value)

    return JsonResponse({'error': 'Invalid request'}, status=400)
