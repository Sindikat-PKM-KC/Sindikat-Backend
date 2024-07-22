from django.urls import path
from .views import AudioUploadView, AudioListView, AudioFileDownloadView

urlpatterns = [
    path("audios/upload/", AudioUploadView.as_view(), name="audio-upload"),
    path("audios/<int:pk>/", AudioFileDownloadView.as_view(), name="audio-download"),
    path("audios/", AudioListView.as_view(), name="audio-list")
]
