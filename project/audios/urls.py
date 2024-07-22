from django.urls import path
from .views import AudioUploadView, AudioListView, AudioFilePlayView

urlpatterns = [
    path("audios/upload/", AudioUploadView.as_view(), name="audio-upload"),
    path("audios/<str:pk>/", AudioFilePlayView.as_view(), name="audio-play"),
    path("audios/", AudioListView.as_view(), name="audio-list")
]
