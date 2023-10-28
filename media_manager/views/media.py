from django.shortcuts import render, redirect, reverse

from media_manager.models import MediaFile

# repositories
from media_manager.repositories import MediaFileRepository, NotificationsRepository

# forms
from media_manager.forms import ManagerCreateMediaFileForm, ManagerUpdateMediaFileForm, DeleteMediaFileForm, \
    AdminCreateMediaFileForm, AdminUpdateMediaFileForm


def create_and_store_media(request):
    if request.user is not None and request.user.is_authenticated:
        if request.method == "GET":

            if request.user.is_super_admin:
                media_form = AdminCreateMediaFileForm()
            else:
                media_form = ManagerCreateMediaFileForm()

            context = {
                "form": media_form
            }

            return render(request, "media_manager/media/media_file_create.html", context)

        elif request.method == "POST":

            if request.user.is_super_admin is True:
                media_form = AdminCreateMediaFileForm(request.POST, request.FILES)
            else:
                media_form = ManagerCreateMediaFileForm(request.POST, request.FILES)

            if media_form.is_valid():
                if request.user.is_super_admin is True:
                    MediaFileRepository.create(media_form.cleaned_data)
                else:
                    media_form.cleaned_data["organisation"] = request.user.organisation.id
                    source_media = MediaFileRepository.create(media_form.cleaned_data)

                    NotificationsRepository.create({
                        "user": request.user.id,
                        "media": source_media.id,
                        "description": f"{request.user.username} fait une demande d'ajouter un fichier media "
                    })

                return redirect(reverse("list_media"))
            else:
                context = {
                    "form": media_form
                }

                return render(request, "media_manager/media/media_file_create.html", context)
    else:
        return redirect(reverse("auth_login"))


def show_media(request, media_id):
    if request.user is not None and request.user.is_authenticated:
        if request.method == "GET":
            try:
                media = MediaFileRepository.find_one(media_id)

                context = {
                    "media": media,
                    "form": DeleteMediaFileForm(media.to_json)
                }
                return render(request, "media_manager/media/media_file_details.html", context)
            except MediaFile.DoesNotExist:

                return redirect(reverse("error_404"))
    else:
        return redirect(reverse("auth_login"))


def edit_and_update_media(request, media_id):
    if request.user is not None and request.user.is_authenticated:
        if request.method == "GET":
            try:
                media = MediaFileRepository.find_one(media_id)
            except MediaFile.DoesNotExist:
                return redirect("model_not_found_error")

            if request.user.is_super_admin is True:
                media_form = AdminUpdateMediaFileForm(media.to_json)
            else:
                media_form = ManagerUpdateMediaFileForm(media.to_json)

            context = {
                "form": media_form,
                "media_id" : media_id
            }

            return render(request, "media_manager/media/media_file_edit.html", context)

        elif request.method == "POST":

            if request.user.is_super_admin is True:
                media_form = AdminUpdateMediaFileForm(request.POST)
            else:
                media_form = ManagerUpdateMediaFileForm(request.POST)

            if media_form.is_valid():
                media_id = media_form.cleaned_data.get("id")
                media = MediaFileRepository.find_one(media_id)
                MediaFileRepository.update(media_id, media_form.cleaned_data)

                # if request.user.is_super_admin is False:
                #     NotificationsRepository.create({
                #         "user": request.user.id,
                #         "source": media.id,
                #         "description": f"{request.user} fait une demande pour modifier un fichier media "
                #     })

                return redirect(reverse("show_media", kwargs={"media_id": media_id}))
            else:

                print("formulaire invalid")
                context = {
                    "form": media_form,
                    "media_id" : media_id
                }

                return render(request, "media_manager/media/media_file_edit.html", context)
    else:
        return redirect(reverse("auth_login"))


def list_media(request):
    if request.method == "GET":

        if request.user is not None and request.user.is_authenticated:
            if request.user.is_super_admin is False:
                authenticated_user = request.user
                organisation = authenticated_user.organisation
                # medias = MediaFileRepository.find_by_organisation_id(organisation_id=organisation.id)
                audios = MediaFileRepository.find_all_audio(organisation_id=organisation.id, count=4)
                videos = MediaFileRepository.find_all_video(organisation_id=organisation.id, count=4)
                context = {
                    "audios": audios,
                    "videos": videos
                }
                return render(request, "media_manager/media/media_file_list.html", context)
            else:
                # medias = MediaFileRepository.find_all()
                audios = MediaFileRepository.find_all_audio(count=4)
                videos = MediaFileRepository.find_all_video(count=4)
                context = {
                    "audios": audios,
                    "videos": videos
                }
                return render(request, "media_manager/media/media_file_list.html", context)
        else:
            return redirect(reverse("auth_login"))


def delete_media(request, media_id):
    if request.user is not None and request.user.is_authenticated:
        if request.method == "POST":
            media_form = DeleteMediaFileForm(request.POST)
            print(request.POST)

            if media_form.is_valid():
                if request.user.is_super_admin:
                    MediaFileRepository.delete(media_form.cleaned_data.get("id"))

                elif request.user.is_super_admin is False:
                    media = MediaFileRepository.find_one(media_id)
                    NotificationsRepository.create({
                        "user": request.user.id,
                        "media": media.id,
                        "request_type" : "deletion-request",
                        "description": f"{request.user} fait une demande de suppresion d'une source media "
                    })

                return redirect(reverse("list_media"))
            else:
                context = {
                    "form": media_form
                }
                return render(request, "", context)
    else:
        return redirect(reverse("auth_login"))


def list_media_video(request):
    if request.method == "GET":

        if request.user is not None and request.user.is_authenticated:
            if request.user.is_super_admin is False:
                authenticated_user = request.user
                organisation = authenticated_user.organisation
                medias = MediaFileRepository.find_all_video(organisation_id=organisation.id)
                context = {
                    "medias": medias
                }
                return render(request, "media_manager/media/video_list.html", context)
            else:
                medias = MediaFileRepository.find_all_video()
                grouped_medias = {}

                for media in medias:
                    if media.organisation.name in grouped_medias.keys():
                        grouped_medias[media.organisation.name].append(media)
                    else:
                        grouped_medias[media.organisation.name] = [media]

                context = {
                    "medias": grouped_medias
                }
                return render(request, "media_manager/media/video_list.html", context)
        else:
            return redirect(reverse("auth_login"))


def list_media_audio(request):
    if request.method == "GET":

        if request.user is not None and request.user.is_authenticated:
            if request.user.is_super_admin is False:
                authenticated_user = request.user
                organisation = authenticated_user.organisation
                medias = MediaFileRepository.find_all_audio(organisation_id=organisation.id)
                context = {
                    "medias": medias
                }
                return render(request, "media_manager/media/audio_list.html", context)
            else:
                medias = MediaFileRepository.find_all_audio()
                # group medias by branches
                grouped_medias = {}

                for media in medias:
                    if media.organisation.name in grouped_medias.keys():
                        grouped_medias[media.organisation.name].append(media)
                    else:
                        grouped_medias[media.organisation.name] = [media]

                context = {
                    "medias": grouped_medias
                }
                return render(request, "media_manager/media/audio_list.html", context)
        else:
            return redirect(reverse("auth_login"))


def show_media_video(request, video_id):
    if request.method == "GET":
        try:
            video = MediaFileRepository.find_one(video_id)
            context = {
                "video": video
            }
            return render(request, "media_manager/media/show_video.html", context)
        except MediaFile.DoesNotExist:
            return redirect(reverse("error_404"))


def show_media_audio(request, audio_id):
    if request.method == "GET":
        try:
            audio = MediaFileRepository.find_one(audio_id)
            context = {
                "audio": audio
            }
            return render(request, "media_manager/media/show_audio.html", context)
        except MediaFile.DoesNotExist:
            return redirect(reverse("error_404"))
