from django.urls import path
from portal import views

urlpatterns = [
    path('', views.home, name="index"),
    path('medias/<int:media_id>', views.media_file_detail, name="detail_media"),
    path('medias/videos/?branche=<str:branche_name>', views.list_videos, name="visitor_list_videos"),
    path('medias/audios/?branche=<str:branche_name>', views.list_audios, name="visitor_list_audios"),

]
