from django.shortcuts import render
from django.http import HttpRequest, HttpResponse
from rest_framework.response import Response
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.permissions import IsAuthenticated, IsAdminUser, AllowAny
from rest_framework.generics import GenericAPIView
from rest_framework_simplejwt.tokens import RefreshToken
from .serializers import AdminLoginSerializer, UserRegisterSerializer, UserLoginSerializer, UserProfileSerializer, UpdateProfileSerializer
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from accounts.models import UserModel


# Create your views here.

# ADMIN RELATED

class AdminLoginView(GenericAPIView):
    permission_classes = [AllowAny]
    serializer_class = AdminLoginSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        return Response(
            {
                "msg": "Login Successful",
                **serializer.validated_data
            }
        )


class AdminLogoutView(GenericAPIView):
    serializer_class = UserLoginSerializer
    def post(self, request):
        try:
            refresh_token = request.data["refresh"]
            token = RefreshToken(refresh_token)
            token.blacklist()
            return Response({"msg": "Logout Successful"}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response(
                {"msg": "Invalid refresh token"}, status=status.HTTP_400_BAD_REQUEST
            )


# USER RELATED

class UserRegisterView(GenericAPIView):
    serializer_class = UserRegisterSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        return Response(
            {
                "msg": "User Created, Perform login",
                # **serializer.validated_data
            }, status=status.HTTP_201_CREATED
        )


class UserLoginView(GenericAPIView):
    serializer_class = UserLoginSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        return Response(
            {
                "msg": "Login Successful",
                **serializer.validated_data
            }
        )


class UserLogoutView(GenericAPIView):
    serializer_class = UserLoginSerializer

    def post(self, request):
        try:
            refresh_token = request.data["refresh"]
            token = RefreshToken(refresh_token)
            token.blacklist()
            return Response({"msg": "Logout Successful"}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response(
                {"msg": "Invalid refresh token"}, status=status.HTTP_400_BAD_REQUEST
            )


class UserProfileView(GenericAPIView):
    serializer_class = UserProfileSerializer
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        user_id = request.user.id
        user = UserModel.objects.get(id=user_id)
        serializer = self.get_serializer(user)
        return Response(serializer.data)

    def patch(self, request, *args, **kwargs):
        user_id = request.user.id
        serializer = UpdateProfileSerializer(data=request.data, partial=True, context={'user_id': user_id})
        serializer.is_valid(raise_exception=True)
        return Response(serializer.data)


