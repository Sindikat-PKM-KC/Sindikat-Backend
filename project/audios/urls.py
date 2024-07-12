from django.urls import path
from .views import AudioUploadView, AudioListView

urlpatterns = [
    path("audios/upload/", AudioUploadView.as_view(), name="audio-upload"),
    path("audios/", AudioListView.as_view(), name="audio-list")
]
