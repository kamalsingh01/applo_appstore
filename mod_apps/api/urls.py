from django.urls import path, include
from .views import (AddAppView, AppListView , AdminAppListView, AdminAppView,
                    UserAppView,GetSubCategoryView, GetCategoryView,
                    AddCategoryView, AddSubCategoryView, DownloadView, DownloadListView
                    )

urlpatterns = [
    path('admin/new/', AddAppView().as_view(), name='add-app'),
    path('admin/details/<int:pk>/', AdminAppView().as_view(), name='admin_app-detail'),
    path('home/', AppListView, name = 'app-list'),
    path('admin/',AdminAppListView().as_view(), name="admin-apps"),
    path('user/detail/<int:pk>/', UserAppView, name = 'user_app_detail'),
    #path('user/',UserAppListView().as_view(), name="user-apps")

    #category
    path('category/list/', GetCategoryView, name = 'category_list'),
    path('category/add/', AddCategoryView.as_view(), name = 'add_category'),
    #subcategory
    path('subcategory/list/', GetSubCategoryView.as_view(), name = 'subcategory_list'),
    path('subcategory/add/', AddSubCategoryView.as_view(), name = 'add_category'),

    #download
    path('user/download/<int:pk>/', DownloadView.as_view(), name = 'app_download'),
    path('user/download/list/', DownloadListView.as_view(), name = 'download_list')

]