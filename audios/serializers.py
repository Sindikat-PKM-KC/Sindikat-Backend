from rest_framework import serializers
from .models import Audio


class AudioSerializer(serializers.ModelSerializer):
    class Meta:
        model = Audio
        fields = "__all__"

    def validate_file(self, value):
        if not value.name.endswith((".wav", ".mp3", ".m4a")):
            raise serializers.ValidationError("File is not a valid audio format")
        return value
