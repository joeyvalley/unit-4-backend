from django.contrib import admin
from django.urls import path, include

from rest_framework import routers
from app.views import PostViewSet, ProfileViewSet, UserViewSet, apiOverview, mainFeed, individualPost, GetUser, GetPostImage, GetProfilePicture
# from rest_framework_simplejwt.views import (
#     TokenObtainPairView,
#     TokenRefreshView,
# )

# router = routers.DefaultRouter()
# router.register(r'user', UserViewSet)
# router.register(r'posts', PostViewSet)
# router.register(r'profile', ProfileViewSet)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', apiOverview, name="api-endpoints"),
    path('api/home/', mainFeed, name="main-feed"),
    path('api/post/<str:post_id>', individualPost, name="individual-post"),
    path('api/users/<str:user_id>', GetUser, name="user-profile"),
    path('posts/<str:img>', GetPostImage, name="see-image"),
    path('avatars/<str:img>', GetProfilePicture, name="see-image")
    # path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    # path('', include(router.urls)),
]
