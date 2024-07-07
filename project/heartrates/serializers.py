from rest_framework import serializers


class AdultHeartRateSerializer(serializers.Serializer):
    type = serializers.IntegerField(required=True)

    def validate_type(self, value):
        if value not in [0, 1]:
            raise serializers.ValidationError("The type field must be either 0 or 1.")
        return value


class ChildHeartRateSerializer(serializers.Serializer):
    type = serializers.IntegerField(required=True)

    def validate_type(self, value):
        if value not in [0, 1]:
            raise serializers.ValidationError("The type field must be either 0 or 1.")
        return value

    
