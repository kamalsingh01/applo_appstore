from django.db import models
from accounts.models import UserModel


class CategoryType(models.Choices):
    EDUCATION = "Education"
    BUSINESS = 'Business'
    ENTERTAINMENT = 'Entertainment'
    LIFESTYLE = 'Lifestyle'
    SHOPPING = 'Shopping'


class Category(models.Model):
    id = models.AutoField(primary_key=True, editable=False)
    name = models.CharField(max_length=100,  null=True, unique=True)

    objects = models.manager

    def __str__(self):
        return self.name


class SubCategory(models.Model):
    id = models.AutoField(primary_key=True, editable=False)
    name = models.CharField(max_length=100, unique=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)

    objects = models.manager


    def __str__(self):
        return self.name


class App(models.Model):
    id = models.AutoField(primary_key=True, editable=False)
    name = models.CharField(max_length=75, null=False, unique=True)
    link = models.URLField(max_length=250, null=False)
    points = models.IntegerField(default=0, null=False)
    added_by = models.ForeignKey(UserModel, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.DO_NOTHING)
    subcategory = models.ForeignKey(SubCategory, on_delete=models.DO_NOTHING)
    app_image = models.ImageField(upload_to="app/", null = True)

    objects = models.manager

    def __str__(self):
        return self.name


class Download(models.Model):
    id = models.AutoField(primary_key=True, editable=False)
    app = models.ForeignKey(App, on_delete=models.CASCADE)
    user = models.ForeignKey(UserModel, on_delete=models.CASCADE)
    status = models.BooleanField(default=False)
    screenshot = models.ImageField(upload_to="mod_apps/files/screenshot", blank=True, default=None)

    objects = models.manager

    class Meta:
        unique_together = ("app", "user")
