from app.views import *
from django.contrib import admin
from django.urls import path
from rest_framework_simplejwt.views import (
    TokenObtainPairView, TokenRefreshView)

urlpatterns = [
    # Admin
    path('admin/', admin.site.urls),
    # Client Side
    path('', defaultView, name="default"),
    path('api/', apiOverview, name="api-endpoints"),
    path('api/home/', mainFeed, name="main-feed"),
    path('api/post/<str:post_id>', individualPost, name="individual-post"),
    path('api/users/<str:user_id>', GetUser, name="user-profile"),
    path('posts/<str:img>', GetPostImage, name="see-image"),
    path('avatars/<str:img>', GetProfilePicture, name="see-image"),
    path('api/create-profile', CreateProfile, name="create-profile"),
    path('api/create-post', CreatePost, name="create-post"),

    # Authentication
    path('api/token/', CustomTokenObtainPairView.as_view(),
         name='token_obtain_pair'),
    path('api/edit-post/', like, name="like-post"),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('api/token/verify/', CustomTokenVerifyView.as_view(), name='token_verify'),
]
