from django.contrib import admin
from django.urls import path, include

from rest_framework import routers
from app.views import PostViewSet, ProfileViewSet, UserViewSet, MainFeed, GetUser

from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
    TokenVerifyView
)


router = routers.DefaultRouter()
router.register(r'user', UserViewSet)
router.register(r'posts', PostViewSet)
router.register(r'profile', ProfileViewSet)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include(router.urls)),
    path('home/', MainFeed),
    path('users/<user_id>/', GetUser),
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('api/token/verify/', TokenVerifyView.as_view(), name='token_verify'),
]
