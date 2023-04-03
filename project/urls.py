from django.contrib import admin
from django.urls import path, include

from rest_framework import routers
from app.views import PostViewSet, ProfileViewSet

router = routers.DefaultRouter()
router.register(r'posts', PostViewSet)
router.register(r'users', ProfileViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('admin/', admin.site.urls)
]
