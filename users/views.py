from .serializers import RegisterSerializer, EmergencyContactSerializer
from .models import User, EmergencyContact
from rest_framework import generics


class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = RegisterSerializer


class EmergencyContactCreateView(generics.CreateAPIView):
    queryset = EmergencyContact.objects.all()
    serializer_class = EmergencyContactSerializer

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
