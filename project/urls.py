from django.contrib import admin
from django.urls import path, include

from rest_framework import routers
from app.views import PostViewSet, ProfileViewSet, UserViewSet, MainFeed, GetUser

from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

router = routers.DefaultRouter()
router.register(r'user', UserViewSet)
router.register(r'posts', PostViewSet)
router.register(r'profile', ProfileViewSet)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('', include(router.urls)),
    path('home/', MainFeed),
    path('users/<user_id>/', GetUser)
]
