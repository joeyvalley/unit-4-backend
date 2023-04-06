from app.views import *
from django.contrib import admin
from django.urls import path

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
    path('api/edit-post/', like, name="like-post"),

    # Authentication
    path('api/login/', CustomAuthToken.as_view(),  name='create-token'),
    path('api/verify/', MyView.as_view(), name='my-view'),
]
