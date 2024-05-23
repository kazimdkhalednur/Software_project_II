from drf_spectacular.utils import OpenApiExample, OpenApiResponse, extend_schema
from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.authtoken.views import ObtainAuthToken as DefaultObtainAuthToken
from rest_framework.generics import CreateAPIView
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView

from .serializers import (
    AuthTokenSerializer,
    ChangePasswordSerializer,
    SignUpSerializer,
    UserInfoSerializer,
)


@extend_schema(
    responses={
        201: OpenApiResponse(
            response=SignUpSerializer(),
            examples=[
                OpenApiExample(
                    "Success Response",
                    value={"message": "User Created Successfully"},
                    response_only=True,
                    status_codes=["201"],
                ),
            ],
        ),
    }
)
class SignUpView(CreateAPIView):
    serializer_class = SignUpSerializer
    permission_classes = [AllowAny]

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(
            {"message": "User Created Successfully"},
            status=status.HTTP_201_CREATED,
            headers=headers,
        )


class ObtainAuthToken(DefaultObtainAuthToken):
    serializer_class = AuthTokenSerializer
    permission_classes = [AllowAny]

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(
            data=request.data, context={"request": request}
        )
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data["user"]
        token, created = Token.objects.get_or_create(user=user)
        return Response({"token": token.key, "role": user.role})


class UserInfoView(APIView):
    serializer_class = UserInfoSerializer

    def get(self, request, *args, **kwargs):
        """Get User Info"""
        user = request.user
        serializer = self.serializer_class(user)
        return Response(serializer.data)

    def post(self, request, *args, **kwargs):
        """Update User Info"""
        user = request.user
        serializer = self.serializer_class(user, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)


@extend_schema(
    responses={
        201: OpenApiResponse(
            response=ChangePasswordSerializer(),
            examples=[
                OpenApiExample(
                    "Success Response",
                    value={"message": "Password changed successfully"},
                    response_only=True,
                    status_codes=["201"],
                ),
            ],
        ),
    }
)
class ChangePasswordAPIView(APIView):
    serializer_class = ChangePasswordSerializer

    def put(self, request, *args, **kwargs):
        user = request.user
        serializer = self.serializer_class(user, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(
            {"message": "Password changed successfully"},
        )
