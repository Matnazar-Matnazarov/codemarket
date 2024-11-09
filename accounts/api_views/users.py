from rest_framework import serializers
from django.contrib.auth import get_user_model
from django.core.cache import cache
from google.oauth2 import id_token
from google.auth.transport import requests
from django.conf import settings

User = get_user_model()


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ("id", "email", "first_name", "last_name")
        read_only_fields = ("email",)


class UserRegistrationSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ("email", "password", "first_name", "last_name")

    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)
        return user


class EmailVerificationSerializer(serializers.Serializer):
    token = serializers.CharField()

    def validate_token(self, value):
        cache_key = f"verification_token_{value}"
        email = cache.get(cache_key)

        if not email:
            raise serializers.ValidationError("Invalid or expired verification token.")

        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            raise serializers.ValidationError("User not found.")

        # Delete token from cache
        cache.delete(cache_key)

        self.validated_data["user"] = user
        return value


class GoogleAuthSerializer(serializers.Serializer):
    token = serializers.CharField()

    def validate_token(self, value):
        try:
            idinfo = id_token.verify_oauth2_token(
                value, requests.Request(), settings.GOOGLE_OAUTH2_CLIENT_ID
            )

            email = idinfo["email"]

            user, created = User.objects.get_or_create(
                email=email,
                defaults={
                    "first_name": idinfo.get("given_name", ""),
                    "last_name": idinfo.get("family_name", ""),
                    "is_active": True,
                },
            )

            self.validated_data["user"] = user
            return value

        except ValueError:
            raise serializers.ValidationError("Invalid token")
