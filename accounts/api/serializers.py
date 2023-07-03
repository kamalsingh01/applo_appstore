from rest_framework import serializers
from accounts.models import UserModel
from rest_framework_simplejwt.tokens import RefreshToken
from django.db import IntegrityError
from mod_apps.models import App
from django.contrib.auth import authenticate
from accounts.manager import UserManager
from django.core.exceptions import ObjectDoesNotExist


# from django.contrib.auth.hashers import check_password


class LoginSerializer(serializers.Serializer):
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


# USER RELATED

class UserRegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserModel
        fields = ['first_name', 'last_name', 'email', 'username', 'phone_number', 'user_role', 'app_points',
                  'profile_image', 'password']
        write_only_fields = ['password']
        read_only_fields = ['app_points', 'user_role']

    def validate(self, attrs):
        try:
            password = attrs['password']
            attrs.pop("password", None)
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


class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserModel
        fields = ['first_name', 'last_name', 'username', 'email', 'phone_number', 'user_role', 'app_points',
                  'profile_image']
        read_only_fields = ['app_points', 'user_role']




class UpdateProfileSerializer(serializers.Serializer):
    first_name = serializers.CharField(max_length=100)
    last_name = serializers.CharField(max_length=100)
    username = serializers.CharField(max_length=100)
    email = serializers.EmailField(max_length=100)
    phone_number = serializers.IntegerField()
    app_points = serializers.IntegerField()
    profile_image = serializers.ImageField()

    def validate(self, attrs):
        user_id = self.context.get('user_id')
        user = UserModel.objects.get(id=user_id)
        if user:
            try:
                user.first_name = attrs.get('first_name', user.first_name)
                user.last_name = attrs.get('last_name', user.last_name)
                user.username = attrs.get('username', user.username)
                user.email = attrs.get('email', user.email)
                user.phone_number = attrs.get('phone_number', user.phone_number)
                user.profile_image = attrs.get('profile_image', user.profile_image)
                user.save()
                return user
            except IntegrityError:
                raise serializers.ValidationError({"msg": "field data already exist"})

    def update(self, instance, validated_data):
        instance.app_points = instance.app_points + validated_data.points
        instance.save()
        return instance
