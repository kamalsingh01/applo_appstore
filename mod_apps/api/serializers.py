from rest_framework import serializers
from mod_apps.models import App, Category, SubCategory, Download
from django.db import IntegrityError
from accounts.models import UserModel


class NewAppResponseSerializer(serializers.ModelSerializer):
    class Meta:
        model = App
        fields = ['id', 'name', 'link', 'category', 'subcategory', 'points', 'app_image', 'added_by']
        read_only_fields = ['added_by']


class NewAppSerializer(serializers.Serializer):
    name = serializers.CharField(max_length=100, required=True)
    link = serializers.URLField(required=True)
    category = serializers.IntegerField(required=True)
    subcategory = serializers.IntegerField(default=None)
    points = serializers.IntegerField(required=True)
    app_image = serializers.ImageField()

    def validate(self, attrs):
        user_id = self.context.get('user_id')
        category_id = attrs.get('category')
        subcategory_id = attrs.get('subcategory')
        try:
            app = App(name=attrs['name'],
                      link=attrs['link'],
                      category_id=attrs['category'],
                      subcategory_id=attrs['subcategory'],
                      points=attrs['points'],
                      app_image=attrs['app_image'],
                      added_by_id=user_id,
                      )
            app.save()
            return app
        except Category.DoesNotExist:
            raise serializers.ValidationError({"error": "invalid category"})
        except SubCategory.DoesNotExist:
            raise serializers.ValidationError({"error": "invalid subcategory"})
        except IntegrityError:
            raise serializers.ValidationError({"error": "App Already Exist"})


class GetAppSerializer(serializers.ModelSerializer):
    class Meta:
        model = App
        fields = ['id', 'name', 'link', 'category', 'points', 'added_by']
        read_only_fields = ['added_by']

    def validate(self, attrs):
        # user_id = self.context.get('user_id')
        # user = UserModel.objects.get(id=user_id)

        name = attrs.get('name')
        if name:
            # Checking if an app with the same name already exists
            existing_app = App.objects.filter(name=name).exclude(id=self.instance.id).first()
            if existing_app:
                raise serializers.ValidationError({'error': 'An app with the same name already exists.'})

        # attrs['added_by'] = user
        return attrs


# Category Related
class GetCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'


class AddCategorySerializer(serializers.Serializer):
    name = serializers.CharField(required=True)

    def validate(self, attrs):
        try:
            category = Category(
                name=attrs['name']
            )
            category.save()
            return category
        except IntegrityError:
            raise serializers.ValidationError({"error": "Category Already Exists"})


# Sub-Category
class GetSubCategorySerializer(serializers.Serializer):
    category_id = serializers.IntegerField(required=True)

    def validate(self, attrs):
        category_id = attrs['category_id']
        queryset = SubCategory.objects.filter(category_id=category_id)
        print(queryset)
        if len(queryset) != 0:
            sub_category_list = [
                {'id': sc.id, 'name': sc.name} for sc in queryset
            ]
            return sub_category_list
        else:
            raise serializers.ValidationError({"error": "Sub-category doesn't exist"})


class AddSubCategorySerializer(serializers.Serializer):
    name = serializers.CharField(required=True)
    category_id = serializers.IntegerField(required=True)

    def validate(self, attrs):
        try:
            subcategory = SubCategory(
                name=attrs['name'],
                category_id=attrs['category_id'],
            )
            subcategory.save()
            return subcategory
        except IntegrityError:
            raise serializers.ValidationError({"error": "Sub-Category Already Exists"})


# Download

class DownloadListSerializer(serializers.ModelSerializer):
    app = NewAppResponseSerializer()

    class Meta:
        model = Download
        fields = ['id', 'app', 'status', 'screenshot', 'user_id']


class TaskListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Download
        fields = ['id', 'status', 'screenshot', 'app_id', 'user_id']


class TaskSerializer(serializers.Serializer):
    screenshot = serializers.ImageField()

    def validate(self, attrs):
        user_id = self.context.get('user_id')
        download_id = self.context.get('down_id')
        download = Download.objects.get(id=download_id)
        if download.user_id == user_id:
            download.screenshot = attrs.get('screenshot', download.screenshot)
            download.status = True
            download.save()
        else:
            raise serializers.ValidationError({"msg": "Not allowed to complete task"})
        return download
