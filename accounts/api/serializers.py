from rest_framework import serializers
from accounts.models import UserModel
from rest_framework_simplejwt.tokens import RefreshToken
from django.db import IntegrityError
from django.contrib.auth import authenticate
from accounts.manager import UserManager
from django.core.exceptions import ObjectDoesNotExist
# from django.contrib.auth.hashers import check_password


# ADMIN RELATED
class AdminLoginSerializer(serializers.Serializer):
    username = serializers.CharField(required=True)
    password = serializers.CharField(
        style={
            "input_type": "password"
        },
        write_only=True
    )

    def validate(self, attrs):

        try:
            user = UserModel.objects.get(username=attrs['username'])
        except UserModel.DoesNotExist:
            raise serializers.ValidationError({" error ": " User doesn't Exist "})
        if user:
            # check_user = authenticate(username = attrs['username'], password = attrs['password'])
            if user.is_superuser and user.is_staff:
                attrs['data_type'] = 'admin'
            else:
                raise serializers.ValidationError({" error " : " Not an Admin Account "})
            if user.check_password(attrs['password']):
                refresh = RefreshToken.for_user(user)
                return {
                    "token": {
                        "refresh": str(refresh),
                        "access": str(refresh.access_token)
                    }
                }
            else:
                raise serializers.ValidationError({"error": "Invalid Password"})


# USER RELATED

class UserRegisterSerializer( serializers.ModelSerializer):

    class Meta:
        model = UserModel
        fields = ['first_name', 'last_name', 'email', 'username', 'phone_number','user_role', 'app_points','profile_image', 'password']
        write_only_fields = ['password']
        read_only_fields = ['app_points', 'user_role']

    def validate(self, attrs):
        try:
            password = attrs['password']
            attrs.pop("password",None)
            user = UserModel(**attrs)
            user.set_password(password)
            user.save()

            return user

            # refresh = RefreshToken.for_user(user)
            # return {
            #     "token": {
            #         "refresh": str(refresh),
            #         "access": str(refresh.access_token)
            #     }
            # }
        except IntegrityError:
            raise serializers.ValidationError({"error": "User already exists"})

class UserLoginSerializer(serializers.Serializer):
    username = serializers.CharField(required=True)
    password = serializers.CharField(
        style={
            "input_type": "password"
        },
        write_only=True
    )

    def validate(self, attrs):
        try:
            user = UserModel.objects.get(username=attrs['username'])
        except UserModel.DoesNotExist:
            raise serializers.ValidationError({"error": "User doesn't Exist"})
        if user:
            print(attrs['password'])
            if user.check_password(attrs['password']):
                refresh = RefreshToken.for_user(user)
                # creating token manually using JWT and returning once user successfully registers
                return {
                    "token": {
                        "refresh": str(refresh),
                        "access": str(refresh.access_token)
                    }
                }
            else:
                raise serializers.ValidationError({"error": "Invalid Password"})