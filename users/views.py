from rest_framework import generics
from .serializers import RegisterSerializer, EmergencyContactSerializer
from .models import EmergencyContact, CustomUser


# Create your views here.
class RegisterView(generics.CreateAPIView):
    queryset = CustomUser.objects.all()
    serializer_class = RegisterSerializer


class EmergencyContactCreateView(generics.CreateAPIView):
    queryset = EmergencyContact.objects.all()
    serializer_class = EmergencyContactSerializer

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
