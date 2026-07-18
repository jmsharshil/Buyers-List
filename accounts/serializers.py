from rest_framework import serializers
from .models import User


class RegisterSerializer(serializers.ModelSerializer):
    pin = serializers.CharField(write_only=True, min_length=4, max_length=8)

    class Meta:
        model = User
        fields = [
            "email",
            "pin",
        ]

    def create(self, validated_data):
        pin = validated_data.pop("pin")
        return User.objects.create_user(pin=pin, **validated_data)
    
from django.contrib.auth import authenticate


class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    pin = serializers.CharField()

    def validate(self, attrs):
        email = attrs.get("email")
        pin = attrs.get("pin")

        user = authenticate(email=email, password=pin)

        if not user:
            raise serializers.ValidationError("Invalid email or PIN")

        attrs["user"] = user
        return attrs