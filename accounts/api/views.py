from django.shortcuts import render
from django.http import HttpRequest, HttpResponse
from rest_framework.response import Response
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.permissions import IsAuthenticated, IsAdminUser, AllowAny
from rest_framework.generics import GenericAPIView
from rest_framework_simplejwt.tokens import RefreshToken
from .serializers import  UserRegisterSerializer, UserProfileSerializer, UpdateProfileSerializer, LoginSerializer
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from accounts.models import UserModel
from rest_framework.parsers import MultiPartParser, FormParser


# Create your views here.

class LoginView(GenericAPIView):
    serializer_class = LoginSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        return Response(
            {
                "msg": "Login Successful",
                **serializer.validated_data
            }
        )
# ADMIN RELATED


class LogoutView(GenericAPIView):

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


class UserProfileView(GenericAPIView):
    serializer_class = UserProfileSerializer
    permission_classes = [IsAuthenticated]
    parser_classes = [MultiPartParser, FormParser]

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


