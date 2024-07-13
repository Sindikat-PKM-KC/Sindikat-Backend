from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.response import Response
from rest_framework import status
from users.models import EmergencyContact
from .serializers import AudioSerializer
from .models import Audio
from pathlib import Path
import requests
import environ
import os

class AudioUploadView(generics.CreateAPIView):
    queryset = Audio.objects.all()
    serializer_class = AudioSerializer
    permission_classes = (IsAuthenticated,)
    parser_classes = (MultiPartParser, FormParser)

    def perform_create(self, serializer):
        location = self.request.data.get('location')
        if not location:
            return Response({"error": "Location is required."}, status=status.HTTP_400_BAD_REQUEST)
        
        audio_instance = serializer.save(user=self.request.user)
        success = self.send_whatsapp_notification(self.request.user, self.request.data.get('location'), audio_instance.file.url)

        # if success:
        #     return Response({"success": 0})
        # else:
        #     return Response({"error": "Failed to send WhatsApp notification"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def send_whatsapp_notification(self, user, location, audio_url):
        try:
            BASE_DIR = Path(__file__).resolve().parent.parent
            env = environ.Env()
            environ.Env.read_env(os.path.join(BASE_DIR, ".env"))

            emergency_contacts = EmergencyContact.objects.filter(user=user)
            phone_numbers = [contact.phone_number for contact in emergency_contacts]
            target = ','.join(phone_numbers)
            audio_url = env("APP_URL") + audio_url

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

            # Dummy response success
            return True
        
        except requests.RequestException as e:
            # Handle any errors that occur during the request to the WA gateway
            print(f"Error sending WhatsApp notification: {e}")
            return False

class AudioListView(generics.ListAPIView):
    queryset = Audio.objects.all()
    serializer_class = AudioSerializer
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        return Audio.objects.filter(user=self.request.user)
