from django.shortcuts import render
from rest_framework import viewsets, status, permissions
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import get_user_model
from django.conf import settings
from ..api_views.users import (
    UserSerializer,
    UserRegistrationSerializer,
    EmailVerificationSerializer,
    GoogleAuthSerializer,
)
from ..tasks import send_verification_email
from ..utils import generate_verification_token

User = get_user_model()


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_permissions(self):
        if self.action in ["create", "verify_email", "google_auth"]:
            return [permissions.AllowAny()]
        return super().get_permissions()

    def get_serializer_class(self):
        if self.action == "create":
            return UserRegistrationSerializer
        if self.action == "verify_email":
            return EmailVerificationSerializer
        if self.action == "google_auth":
            return GoogleAuthSerializer
        return self.serializer_class

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        # Don't save user yet, just get the instance
        user = serializer.save(is_active=False)

        # Generate verification token
        token = generate_verification_token()

        # Send verification email asynchronously
        send_verification_email.delay(user.email, token, expires_in=300)  # 5 minutes

        return Response(
            {"detail": "Verification email sent. Please verify within 5 minutes."},
            status=status.HTTP_201_CREATED,
        )

    @action(detail=False, methods=["post"])
    def verify_email(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        user = serializer.validated_data["user"]
        user.is_active = True
        user.save()

        # Generate JWT tokens
        refresh = RefreshToken.for_user(user)

        return Response(
            {
                "refresh": str(refresh),
                "access": str(refresh.access_token),
            }
        )

    @action(detail=False, methods=["post"])
    def google_auth(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        user = serializer.validated_data["user"]
        refresh = RefreshToken.for_user(user)

        return Response(
            {
                "refresh": str(refresh),
                "access": str(refresh.access_token),
            }
        )
