from rest_framework import serializers
from .models import Audio
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
        file.name = self.generate_unique_filename(file.name)
        audio_instance = Audio.objects.create(**validated_data)
        return audio_instance
    
    def generate_unique_filename(self, filename):
        import uuid
        ext = filename.split('.')[-1]
        return f"{uuid.uuid4()}.{ext}"