from django.urls import path, include

from media_manager.views import media as media_view
from media_manager.views import notifications as notification_view
from media_manager.views import source as source_view

media_urlpatterns = [
    path('', media_view.list_media, name="list_media"),
    path('videos/', media_view.list_media_video, name="list_media_video"),
    path('audios/', media_view.list_media_audio, name="list_media_audio"),
    path('videos/<int:video_id>', media_view.show_media_video, name="show_media_video"),
    path('audios/<int:audio_id>', media_view.show_media_audio, name="show_media_audio"),
    # render media form and store new media
    path('create_media/', media_view.create_and_store_media, name="create_media"),
    path('<int:media_id>/', media_view.show_media, name="show_media"),
    # edit and update media
    path('<int:media_id>/edit', media_view.edit_and_update_media, name="edit_media"),
    path('<int:media_id>/delete', media_view.delete_media, name="delete_media"),
]

notification_urlpatterns = [
    path('', notification_view.notifications_main, name="main_notification"),
    path('<notification_type>', notification_view.list_notifications, name="list_notification"),
    path('<notification_type>/<int:notification_id>/', notification_view.show_notification, name="show_notification"),
    path('<notification_type>/<int:notification_id>/reject', notification_view.reject_notification, name="reject_notification"),
    path('<notification_type>/<int:notification_id>/accept', notification_view.accept_notification, name="accept_notification"),
    path('<notification_type>/<int:notification_id>/delete', notification_view.delete_notification, name="delete_notification"),
]

source_media_urlpatterns = [
    path('', source_view.list_source, name="list_source"),
    # render source media form and store new source media
    path('create_source/', source_view.create_and_store_source, name="create_source"),
    path('<int:source_id>/', source_view.show_source, name="show_source"),
    # edit and update source media
    path('<int:source_id>/edit', source_view.edit_and_update_source, name="edit_source"),
    path('<int:source_id>/delete', source_view.delete_source, name="delete_source"),
]

urlpatterns = [
    path('medias/', include(media_urlpatterns)),
    path('notifications/', include(notification_urlpatterns)),
    path('sources/', include(source_media_urlpatterns))
]
