from .serializers import RegisterSerializer, EmergencyContactSerializer
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework import status


# Create your views here.
class RegisterViewSet(viewsets.ViewSet):
    serializer_class = RegisterSerializer

    def create(self, request):
        serializer = RegisterSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class EmergencyContactCreateViewSet(viewsets.ViewSet):
    def create(self, request):
        serializer = EmergencyContactSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
