from .serializers import RegisterSerializer, EmergencyContactSerializer
from .models import User, EmergencyContact
from rest_framework.response import Response
from rest_framework import status
from .serializers import TokenObtainLifetimeSerializer
from rest_framework import generics
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework.permissions import IsAuthenticated


class CustomTokenObtainPairView(TokenObtainPairView):
    serializer_class = TokenObtainLifetimeSerializer

class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = RegisterSerializer

class EmergencyContactCreateView(generics.CreateAPIView):
    queryset = EmergencyContact.objects.all()
    serializer_class = EmergencyContactSerializer

    def perform_create(self, serializer):
        user_id = self.kwargs.get('id')  # Ambil user_id dari URL parameter
        serializer.save(user_id=user_id)

    def create(self, request, *args, **kwargs):
        user_id = self.kwargs.get('id')
        data = request.data.get('data', [])  # Ambil data dari key 'data'

        # Check if the request data is a list
        if not isinstance(data, list):
            return Response({"detail": "Request data must be a list"}, status=status.HTTP_400_BAD_REQUEST)

        errors = []
        validated_data = []

        for item in data:
            if not isinstance(item, dict):
                errors.append("Each item in the list must be a JSON object")
                continue

            name = item.get('name')
            phone_number = item.get('phone_number')

            if not name or not phone_number:
                errors.append("Each item must have 'name' and 'phone_number' keys")
                continue

            # Validate phone_number is an integer and has 10-15 digits
            try:
                phone_number = int(phone_number)
                if not (10 <= len(str(phone_number)) <= 15):
                    errors.append("Phone number must be an integer with 10-15 digits")
                    continue
            except ValueError:
                errors.append("Phone number must be a valid integer")
                continue

            validated_data.append({"name": name, "phone_number": phone_number})

        if errors:
            return Response({"errors": errors}, status=status.HTTP_400_BAD_REQUEST)

        EmergencyContact.objects.filter(user_id=user_id).delete()

        serializer = self.get_serializer(data=validated_data, many=True)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)  # Memanggil perform_create tanpa user_id

        # Ambil data yang sudah disimpan dalam serializer setelah perform_create
        created_data = serializer.data

        # Tambahkan pesan ke dalam response
        response_data = {
            "data": created_data,
            "message": "Emergency contacts created successfully."
        }

        return Response(response_data, status=status.HTTP_201_CREATED)
    
class EmergencyContactListView(generics.ListAPIView):
    serializer_class = EmergencyContactSerializer
    permission_classes = (IsAuthenticated, )

    def get_queryset(self):
        user = self.request.user  # Ambil user dari request
        return EmergencyContact.objects.filter(user=user)