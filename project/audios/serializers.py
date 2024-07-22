from rest_framework import serializers
from .models import Audio
from .utils import encrypt_file, generate_unique_filename
import uuid


class AudioSerializer(serializers.ModelSerializer):
    location = serializers.URLField(write_only=True, required=True)

    class Meta:
        model = Audio
        fields = ("file", "location")

    def validate_file(self, value):
        if not value.name.endswith((".wav", ".mp3", ".m4a")):
            raise serializers.ValidationError("File is not a valid audio format")
        
        return value

    def create(self, validated_data):
        location = validated_data.pop('location')
        file = validated_data['file']
        file.name = generate_unique_filename(file.name)
        
        audio_instance = Audio.objects.create(**validated_data)
        
        # Encrypt the file after saving
        encrypt_file(audio_instance.file.path)
        
        return audio_instance