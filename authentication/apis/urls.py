from django.urls import path,include
from rest_framework.routers import DefaultRouter

from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

from authentication.apis.views import RegisterUserAPIView,LogoutView,UserViewSet

app_name = 'authentication_apis'

router =DefaultRouter()

router.register('users',UserViewSet, basename="user")

urlpatterns = [
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('register/',RegisterUserAPIView.as_view(),name="user-registration"),
    path('logout/',LogoutView.as_view(),name="logout"),
    path('', include(router.urls)),

]