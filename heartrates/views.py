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
