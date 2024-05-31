import os
from django.conf import settings
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.core.files.storage import default_storage
from django.core.files.base import ContentFile
from .test import track_people_from_video  # 함수가 있는 파일에서 가져오기

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
    return JsonResponse({'error': 'Invalid request'}, status=400)