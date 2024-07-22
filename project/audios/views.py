from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from urllib.parse import urljoin
from django.http import HttpResponse, Http404
from django.shortcuts import get_object_or_404
from users.models import EmergencyContact
from .serializers import AudioSerializer
from .models import Audio
from pathlib import Path
from .utils import decrypt_file
import mimetypes
import requests
import environ
import os

class AudioUploadView(generics.CreateAPIView):
    queryset = Audio.objects.all()
    serializer_class = AudioSerializer
    permission_classes = (IsAuthenticated,)
    parser_classes = (MultiPartParser, FormParser)

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        location = request.data.get('location')
        if not location:
            return Response({"error": "Location is required."}, status=status.HTTP_400_BAD_REQUEST)
        
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        
        audio_instance = serializer.instance
        success = self.send_whatsapp_notification(request.user, location, audio_instance.id)  # Pass audio ID

        if success:
            return Response({"message": "Successfully sent WhatsApp notification"}, status=status.HTTP_201_CREATED, headers=headers)
        else:
            return Response({"message": "Failed to send WhatsApp notification"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR, headers=headers)
    
    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    def send_whatsapp_notification(self, user, location, audio_id):
        try:
            BASE_DIR = Path(__file__).resolve().parent.parent
            env = environ.Env()
            environ.Env.read_env(os.path.join(BASE_DIR, ".env"))

            emergency_contacts = EmergencyContact.objects.filter(user=user)
            phone_numbers = [contact.phone_number for contact in emergency_contacts]
            target = ','.join(phone_numbers)

            # Construct the public URL for the audio file
            audio_url = urljoin(env("APP_URL"), f"api/audios/{audio_id}/")

            message = f"Pesan Darurat dari SINDIKAT\n\nNama Pengguna: {user.name}\nLokasi: {location}\nTautan Audio Scream: {audio_url}\n\nSistem deteksi kejahatan kami telah mendeteksi adanya kemungkinan tindakan kejahatan berdasarkan analisis suara teriakan. Mohon segera cek kondisi pengguna di lokasi yang tertera.\n\nTerima kasih atas perhatian dan kerja samanya."

            wa_gateway_url = "https://api.fonnte.com/send"
            payload = {
                'target': target,
                'message': message,
                'countryCode': '62'
            }
            headers = {
                "Authorization": env("FONNTE_TOKEN")
            }

            response = requests.post(wa_gateway_url, data=payload, headers=headers)
            response.raise_for_status()

            return True
        
        except requests.RequestException as e:
            print(f"Error sending WhatsApp notification: {e}")
            return False
        
class AudioFilePlayView(APIView):
    permission_classes = []  # Make the endpoint accessible without authentication

    def get(self, request, *args, **kwargs):
        file_id = kwargs.get('pk')
        audio_instance = get_object_or_404(Audio, id=file_id)
        file_path = audio_instance.file.path

        if not os.path.exists(file_path):
            raise Http404("File does not exist")

        # Check if the file is already decrypted
        if file_path.endswith(".enc"):
            decrypted_file_path = decrypt_file(file_path)
        else:
            decrypted_file_path = file_path

        # Determine the MIME type
        mime_type, _ = mimetypes.guess_type(decrypted_file_path)
        if mime_type is None:
            mime_type = 'application/octet-stream'

        # Serve the file as a response
        try:
            with open(decrypted_file_path, 'rb') as f:
                response = HttpResponse(f, content_type=mime_type)
                response['Content-Disposition'] = f'inline; filename="{os.path.basename(decrypted_file_path)}"'
                return response
        except Exception as e:
            return HttpResponse(f"Error: {str(e)}", status=500)


class AudioListView(generics.ListAPIView):
    queryset = Audio.objects.all()
    serializer_class = AudioSerializer
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        return Audio.objects.filter(user=self.request.user)
