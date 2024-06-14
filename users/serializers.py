from rest_framework import serializers
from .models import User, EmergencyContact
from rest_framework import serializers
from .models import User, EmergencyContact
from rest_framework.validators import UniqueValidator
from django.contrib.auth.password_validation import validate_password
from django.contrib.auth.hashers import make_password


class RegisterSerializer(serializers.ModelSerializer):
    name = serializers.CharField(required=True)
    email = serializers.EmailField(
        required=True, validators=[UniqueValidator(queryset=User.objects.all())]
    )
    phone_number = serializers.IntegerField(required=True)
    password = serializers.CharField(
        write_only=True, required=True, validators=[validate_password]
    )
    password_confirmation = serializers.CharField(write_only=True, required=True)

    class Meta:
        model = User
        fields = ("name", "email", "phone_number", "password", "password_confirmation")

    def validate(self, attrs):
        if len(str(attrs["phone_number"])) < 10:
            raise serializers.ValidationError(
                {"phone_number": "Phone number must be at least 10 digits."}
            )
        if attrs["password"] != attrs["password_confirmation"]:
            raise serializers.ValidationError(
                {"password": "Password fields didn't match."}
            )
        return attrs

    def create(self, validated_data):
        validated_data.pop("password_confirmation")
        user = User.objects.create(
            name=validated_data["name"],
            email=validated_data["email"],
            phone_number=validated_data["phone_number"],
            password=make_password(validated_data["password"]),
        )
        return user


class EmergencyContactSerializer(serializers.ModelSerializer):
    class Meta:
        model = EmergencyContact
        fields = ("name", "phone_number")
