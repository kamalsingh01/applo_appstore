from django.contrib import admin
from .models import App, Download, Category, SubCategory
# Register your models here.
admin.site.register(App)
admin.site.register(Download)
admin.site.register(Category)
admin.site.register(SubCategory)