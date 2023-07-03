from django.urls import path, include
from .views import (LoginView,
                    LogoutView,
                    UserRegisterView,
                    UserProfileView)
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

urlpatterns = [
    # admin
    path('logout/', LogoutView().as_view(), name="admin_logout"),
    path('login/',LoginView().as_view(),name = 'account-login'),

    # user
    path('user/register/', UserRegisterView().as_view(), name="user_register"),
    path('user/profile/', UserProfileView.as_view(), name='user_profile'),

    # token
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]
