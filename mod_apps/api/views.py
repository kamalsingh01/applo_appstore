from django.shortcuts import render
from rest_framework.exceptions import ValidationError
from django.db import IntegrityError
from rest_framework.generics import GenericAPIView
from rest_framework.response import Response
from mod_apps.models import App, Category, SubCategory, Download
from rest_framework.permissions import IsAuthenticated, IsAdminUser, AllowAny
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework import status
from .serializers import (NewAppSerializer, GetAppSerializer,
                          AddCategorySerializer, GetCategorySerializer,
                          GetSubCategorySerializer, AddSubCategorySerializer,
                          NewAppResponseSerializer, DownloadListSerializer, TaskSerializer, TaskListSerializer)
from accounts.models import UserModel
from accounts.api.serializers import UpdateProfileSerializer
from rest_framework.decorators import api_view, permission_classes
from .permissions import IsAdminAndCreator
from rest_framework.parsers import FormParser, MultiPartParser


# Category
@api_view(["GET"])
def GetCategoryView(request):
    category_list = Category.objects.all()
    serializer = GetCategorySerializer(category_list, many=True)
    return Response(serializer.data)


class AddCategoryView(GenericAPIView):
    # permission_classes = [IsAdminUser, IsAuthenticated]
    serializer_class = AddCategorySerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        return Response(
            {
                "msg": "Category Successfully Added",
            },
            status=status.HTTP_201_CREATED

        )


# Sub-Category

class GetSubCategoryView(GenericAPIView):
    serializer_class = GetSubCategorySerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        sub_categories = serializer.validated_data
        return Response(
            {"sub_categories": sub_categories},
            status=status.HTTP_200_OK
        )


class AddSubCategoryView(GenericAPIView):
    # permission_classes = [IsAdminUser, IsAuthenticated]
    serializer_class = AddSubCategorySerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        return Response(
            {
                "msg": "Sub-Category Successfully Added"
            }
        )


@api_view(["GET"])
def AppListView(request):
    app_list = App.objects.all()
    serializer = NewAppResponseSerializer(app_list, many=True)
    return Response(serializer.data)


class AdminAppListView(GenericAPIView):
    serializer_class = NewAppResponseSerializer
    permission_classes = [IsAdminUser]

    def get(self, request, *args, **kwargs):
        user_id = request.user.id
        app_list = App.objects.filter(added_by=user_id)
        serializer = self.get_serializer(app_list, many=True)
        return Response(serializer.data)


class AddAppView(GenericAPIView):
    serializer_class = NewAppSerializer
    permission_classes = [IsAdminUser]
    parser_classes = [MultiPartParser, FormParser]

    def post(self, request, *args, **kwargs):
        user_id = request.user.id
        serializer = self.get_serializer(data=request.data, context={'user_id': user_id})
        serializer.is_valid(raise_exception=True)
        return Response(
            {
                "msg": "New App created",
                # **serializer.validated_data
            }
        )


class AdminAppView(GenericAPIView):
    serializer_class = GetAppSerializer

    # permission_classes = [IsAdminUser, IsAdminAndCreator]

    def get(self, request, pk, *args, **kwargs):
        try:
            user_id = request.user.id
            app = App.objects.get(id=pk, added_by_id=user_id)
            serializer = self.get_serializer(app)
        except App.DoesNotExist:
            raise ValidationError({"error": "App doesn't Exist"})
        return Response(serializer.data)

    def patch(self, request, pk, *args, **kwargs):
        user_id = request.user.id
        app = App.objects.get(id=pk)
        serializer = self.get_serializer(app, data=request.data, partial=True, context={'user_id': user_id})
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.validated_data, status=status.HTTP_202_ACCEPTED)

    def delete(self, request, pk):
        try:
            app = App.objects.get(id=pk)
            app.delete()
        except App.DoesNotExist:
            raise ValidationError({"error": "App doesn't Exist"})
        return Response(status=status.HTTP_204_NO_CONTENT)


@api_view(["GET"])
@permission_classes([AllowAny])
def UserAppView(request, pk):
    app_detail = App.objects.get(id=pk)
    serializer = NewAppResponseSerializer(app_detail)
    return Response(serializer.data)


class DownloadView(GenericAPIView):
    permission_classes = [IsAuthenticated]

    serializer_class = UpdateProfileSerializer

    def post(self, request, pk, *args, **kwargs):
        user_id = request.user.id
        try:
            download = Download(
                app_id=pk,
                user_id=user_id
            )
            user = UserModel.objects.get(id=user_id)
            app = App.objects.get(id=pk)
            serializer = UpdateProfileSerializer(data=request.data, partial=True,
                                                 context={'user_id': user_id, "app_id": pk})
            download.save()
            serializer.update(user, app)
            return Response({"msg": "App Downloaded"})
        except IntegrityError:
            raise ValidationError({"error": "App already downloaded by the user"})


class DownloadListView(GenericAPIView):
    serializer_class = DownloadListSerializer
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        user_id = request.user.id
        downloads = Download.objects.filter(user_id=user_id)
        serializer = self.get_serializer(downloads, many=True)
        return Response(serializer.data)


class TaskListView(GenericAPIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        user_id = request.user.id
        tasks = Download.objects.filter(user_id=user_id)
        serializer = TaskListSerializer(tasks, many = True)
        return Response(serializer.data)


class TaskView(GenericAPIView):
    serializer_class = TaskSerializer
    permission_classes = [IsAuthenticated]
    parser_classes = [MultiPartParser, FormParser]

    def get(self, request, pk, *args, **kwargs):
        user_id = request.user.id
        task = Download.objects.get(user_id=user_id, id=pk)
        serializer = TaskListSerializer(task)
        return Response(serializer.data)

    def patch(self, request, pk, *args, **kwargs):
        user_id = request.user.id
        serializer = self.get_serializer(data=request.data, partial=True, context={'user_id': user_id, 'down_id': pk})
        serializer.is_valid(raise_exception=True)
        return Response({
            "msg": "Task Completed"
        })
