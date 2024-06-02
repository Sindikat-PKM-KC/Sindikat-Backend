from django.db import models
from django.conf import settings


class Audio(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    file = models.FileField(upload_to="audios/")
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Audio by {self.user.email} at {self.uploaded_at}"
