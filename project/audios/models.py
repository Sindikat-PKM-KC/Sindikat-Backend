from django.db import models
from users.models import User
import uuid

class Audio(models.Model):
    id = models.UUIDField(default=uuid.uuid4, unique=True,
          primary_key=True, editable=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    file = models.FileField(upload_to="audios/", max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.user.name} ##### {self.created_at}"
