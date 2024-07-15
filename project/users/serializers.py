from rest_framework import serializers
from .models import User, EmergencyContact
from rest_framework import serializers
from .models import User, EmergencyContact
from rest_framework.validators import UniqueValidator
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from django.contrib.auth.password_validation import validate_password
from django.contrib.auth.hashers import make_password

class TokenObtainLifetimeSerializer(TokenObtainPairSerializer):
    def validate(self, attrs):
        data = super().validate(attrs)
        
        user = self.user
        data['user'] = {
            'id': user.id,
            'name': user.name,
            'email': user.email,
        }
        return data
    

class RegisterSerializer(serializers.ModelSerializer):
    name = serializers.CharField(required=True)
    email = serializers.EmailField(
        required=True, validators=[UniqueValidator(queryset=User.objects.all())]
    )
    password = serializers.CharField(
        write_only=True, required=True, validators=[validate_password]
    )
    password_confirmation = serializers.CharField(write_only=True, required=True)

    class Meta:
        model = User
        fields = ("name", "email", "password", "password_confirmation")

    def validate(self, attrs):
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
            password=make_password(validated_data["password"]),
        )
        
        # Creating the Emergency Contact
        EmergencyContact.objects.create(
            user=user,
            name="I Gede Widiantara",
            phone_number="082146560178"
        )

        return user

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation['id'] = instance.id
        return representation


class EmergencyContactSerializer(serializers.ModelSerializer):
    class Meta:
        model = EmergencyContact
        fields = ("name", "phone_number")
