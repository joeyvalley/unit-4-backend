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
    path('api/posts/<str:user_id>', GetAllUserPosts, name="get-grid"),
    path('posts/<str:img>', GetPostImage, name="see-image"),
    path('avatars/<str:img>', GetProfilePicture, name="see-image"),
    path('api/create-profile/', CreateProfile, name="create-profile"),
    path('api/create-post/', CreatePost, name="create-post"),
    path('api/like/', like, name="like-post"),
    path('api/dislike/', dislike, name="dislike-post"),
    path('api/create-comment/', createComment, name="create-comment"),
    path('api/sign-up/', SignUp.as_view(), name="sign-up"),

    # Authentication
    path('api/login/', AuthenticateUser.as_view(),  name='create-token'),
    path('api/verify/', VerifyAuthentication.as_view(), name='my-view'),
]
