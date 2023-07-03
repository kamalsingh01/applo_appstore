from django.urls import path, include
from .views import (AddAppView, AppListView , AdminAppListView, AdminAppView,
                    UserAppView,GetSubCategoryView, GetCategoryView,
                    AddCategoryView, AddSubCategoryView, DownloadView, DownloadListView, TaskView, TaskListView
                    )

urlpatterns = [
    path('new/', AddAppView().as_view(), name='add-app'),
    path('admin/<int:pk>/', AdminAppView().as_view(), name='admin_app-detail'),
    path('home/', AppListView, name = 'app-list'),
    path('admin/',AdminAppListView().as_view(), name="admin-apps"),
    path('user/<int:pk>/', UserAppView, name = 'user_app_detail'),

    #category
    path('category/list/', GetCategoryView, name = 'category_list'),
    path('category/add/', AddCategoryView.as_view(), name = 'add_category'),
    #subcategory
    path('subcategory/list/', GetSubCategoryView.as_view(), name = 'subcategory_list'),
    path('subcategory/add/', AddSubCategoryView.as_view(), name = 'add_category'),

    #download
    path('user/download/<int:pk>/', DownloadView.as_view(), name = 'app_download'),
    path('user/download/list/', DownloadListView.as_view(), name = 'download_list'),
    path('user/task/<int:pk>/',TaskView.as_view(), name = 'task-details'),
    path('user/task/list/',TaskListView().as_view(), name = 'task-list')

]