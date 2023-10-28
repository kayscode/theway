from django.shortcuts import render
from media_manager.repositories import MediaFileRepository


# Create your views here.

def home(request):
    if request.method == "GET":
        audios = MediaFileRepository.find_approved_media(media_type="audio",count=10)
        videos = MediaFileRepository.find_approved_media(media_type="video",count=10)
        context = {
            "audios": audios,
            "videos": videos
        }
        return render(request, "portal/index.html", context)


def list_videos(request,branche_name):

    if request.method == "GET":
        if branche_name == 'all':
            videos = MediaFileRepository.find_approved_media("video")
        else:
            videos = MediaFileRepository.filter_by_branche(media_type="video",branche_name=branche_name)

        context = {
            "videos": videos
        }
        return render(request, "portal/video_list.html", context)


def list_audios(request,branche_name):
    print(branche_name)
    if request.method == "GET":
        if branche_name == 'all':
            audios = MediaFileRepository.find_approved_media("audio")
        else:
            audios = MediaFileRepository.filter_by_branche(media_type="audio", branche_name=branche_name)

        context = {
            "audios": audios
        }

        return render(request, "portal/audio_list.html", context)


def media_file_detail(request, media_id):
    context = {
        "media" : MediaFileRepository.find_one(media_id=media_id)
    }
    return render(request, "portal/fichier_media.html",context)
