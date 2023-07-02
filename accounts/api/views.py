from django.shortcuts import render
from django.http import HttpRequest, HttpResponse
from rest_framework.response import Response
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.permissions import IsAuthenticated, IsAdminUser, AllowAny
from rest_framework.generics import GenericAPIView
from rest_framework_simplejwt.tokens import RefreshToken
from .serializers import AdminLoginSerializer, UserRegisterSerializer, UserLoginSerializer
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
                #**serializer.validated_data
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
    # authentication_classes = [JWTAuthentication]

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

@api_view(["GET"])
@permission_classes([IsAuthenticated])
def UserProfileView(request):
    user_id = request.user.id
    user_details = UserModel.objects.get(id = user_id)
    serializer = UserRegisterSerializer(user_details)
    return Response(serializer.data)