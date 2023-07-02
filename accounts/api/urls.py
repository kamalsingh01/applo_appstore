from django.urls import path, include
from .views import (AdminLoginView,
                    AdminLogoutView,
                    UserRegisterView,
                    UserLoginView,
                    UserLogoutView,
                    UserProfileView)
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

urlpatterns = [
    path('admin/login/', AdminLoginView().as_view(), name = "admin_login"),
    path('admin/logout/', AdminLogoutView().as_view(), name = "admin_logout"),
    path('user/register/', UserRegisterView().as_view(), name = "user_register"),
    path('user/login/', UserLoginView().as_view(), name = "user_login" ),
    path('user/profile/', UserProfileView, name = 'user_profile'),
    path('user/logout/', UserLogoutView().as_view(), name = "user-logout"),

    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]