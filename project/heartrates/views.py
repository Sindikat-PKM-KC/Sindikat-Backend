from rest_framework import generics, status
from .serializers import AdultHeartRateSerializer, ChildHeartRateSerializer
from rest_framework.response import Response
from rest_framework.mixins import CreateModelMixin
from rest_framework.permissions import IsAuthenticated
import random
import time


class AdultHeartRateView(CreateModelMixin, generics.GenericAPIView):
    serializer_class = AdultHeartRateSerializer
    permission_classes = (IsAuthenticated,)

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            time.sleep(2)

            type_value = serializer.validated_data["type"]
            if type_value == 0:
                heart_rate = random.randint(60, 100)
                status_message = "normal"
            else:
                heart_rate = random.randint(100, 170)
                status_message = "potentially in danger"

            response_data = {"heart_rate": heart_rate, "status": status_message}
            return Response(response_data, status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ChildHeartRateView(CreateModelMixin, generics.GenericAPIView):
    serializer_class = ChildHeartRateSerializer
    permission_classes = (IsAuthenticated,)

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            time.sleep(2)

            type_value = serializer.validated_data["type"]
            if type_value == 0:
                heart_rate = random.randint(60, 100)
                status_message = "normal"
            else:
                heart_rate = random.randint(100, 170)
                status_message = "potentially in danger"

            response_data = {"heart_rate": heart_rate, "status": status_message}
            return Response(response_data, status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class SendHeartRateView(CreateModelMixin, generics.GenericAPIView):
    permission_classes = (IsAuthenticated,)

    def post(self, request, *args, **kwargs):
        data = request.data.get('data', [])

        # Check if the request data is a list
        if not isinstance(data, list):
            return Response({"detail": "Request data must be a list"}, status=status.HTTP_400_BAD_REQUEST)

        # Check if each item has 'timestamp' and 'heartrate' keys
        for item in data:
            if not isinstance(item, dict):
                return Response({"detail": "Each item in the list must be a JSON object"}, status=status.HTTP_400_BAD_REQUEST)
            if 'timestamp' not in item or 'heartrate' not in item:
                return Response({"detail": "Each item must have 'timestamp' and 'heartrate' keys"}, status=status.HTTP_400_BAD_REQUEST)

        # Simpan data untuk pemrosesan di masa mendatang
        # Misalnya, Anda dapat menyimpan data ke dalam basis data atau antrean untuk diproses oleh model AI di kemudian hari

        # Response sementara bahwa data belum diproses
        return Response({"message": "Data has been received but not yet processed."}, status=status.HTTP_202_ACCEPTED)