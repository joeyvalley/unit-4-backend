
# Models and serializers for admin panel.
from rest_framework.views import APIView
import cloudinary.uploader
from rest_framework.parsers import MultiPartParser, JSONParser
from django.http import Http404, FileResponse
from django.conf import settings
import os
from .models import Comment, Post, Profile
from .serializers import CommentSerializer, PostSerializer, ProfileSerializer, UserSerializer

# Dependencies for Django authorization/authentication.
from django.contrib.auth.models import User
from rest_framework import permissions, viewsets
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from django.contrib.auth.hashers import make_password

# Dependencies for client views
from rest_framework.response import Response
from rest_framework.decorators import api_view


# Admin panel views and serializers.

class CategoryListView(APIView):

    def get(self, request, format=None):
        pass

    def post(self, request, format=None):
        pass


class CommentViewSet(viewsets.ModelViewSet):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer


class PostViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.all()
    serializer_class = PostSerializer


class ProfileViewSet(viewsets.ModelViewSet):
    queryset = Profile.objects.all()
    serializer_class = ProfileSerializer


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer

    def get_permissions(self):
        # allow non-authenticated user to create via POST
        return (permissions.AllowAny() if self.request.method == 'POST' else IsStaffOrTargetUser()),

    def perform_create(self, serializer):
        password = make_password(self.request.data['password'])
        serializer.save(password=password)

    def perform_update(self, serializer):
        password = make_password(self.request.data['password'])
        serializer.save(password=password)


class IsOwnerOrReadOnly(permissions.BasePermission):
    """
    Custom permission to only allow owners of an object to edit it.
    """

    def has_object_permission(self, request, view, obj):
        # Read permissions are allowed to any request,
        # so we'll always allow GET, HEAD or OPTIONS requests,
        # due to we need to decrease the quantity of the product,
        # we'll always allow PUT requests too.
        if request.method in permissions.SAFE_METHODS or request.method == 'PUT':
            return True
        # Write permissions are only allowed to the owner of the snippet.
        return obj.owner == request.user


class IsStaffOrTargetUser(permissions.BasePermission):
    def has_permission(self, request, view):
        # allow user to list all users if logged in user is staff
        return view.action == 'retrieve' or request.user.is_staff

    def has_object_permission(self, request, view, obj):
        # allow logged in user to view own details,
        # allows staff to view all records.
        return obj == request.user or request.user.is_staff


# Client-side views and serializers.
@api_view(['GET'])
def apiOverview(request):
    api_urls = {
        'Main Feed': '/api/home/',
        'User Profile': '/api/users/<str:username>/',
        'Image File': '/posts/<str:img>',

        'Individual Post': '/api/post/<str:post_id>',
        'Create Post': '/api/post/',
        'Update Post': '/api/post/<str:post_id>/',
        'Delete Post': '/api/post/<str:post_id>/',

        'Sign Up': '/api/auth/sign-up/',
        'Sign In': '/api/auth/sign-in/',

        'Edit Profile': '/auth/edit/<str:username>/',
        'Delete Profile': '/auth/delete/<str:username>/'
    }
    return Response(api_urls)

# GET Methods


@api_view(['GET'])
def defaultView(request):
    return Response({'message': 'hello'})


@api_view(['GET'])
def mainFeed(request):
    posts = Post.objects.all()
    serializer = PostSerializer(posts, many=True)
    return Response(serializer.data)


@api_view(['GET'])
def individualPost(request, post_id):
    posts = Post.objects.get(id=post_id)
    serializer = PostSerializer(posts, many=False)
    return Response(serializer.data)


@api_view(['GET'])
def GetUser(request, user_id):
    user = User.objects.get(username=user_id)
    serializer = UserSerializer(user, many=False)
    return Response(serializer.data)


@api_view(['GET'])
def GetPostImage(request, img):
    # Get the path to the image file
    image_path = os.path.join(settings.BASE_DIR, f'posts/{img}')

    # Check if the file exists
    if not os.path.isfile(image_path):
        raise Http404('Image file not found')

    # Create a response that serves the image file
    response = FileResponse(open(image_path, 'rb'))
    response['Content-Type'] = 'image/jpeg'

    return response


@api_view(['GET'])
def GetProfilePicture(request, img):
    # Get the path to the image file
    image_path = os.path.join(settings.BASE_DIR, f'avatars/{img}')

    # Check if the file exists
    if not os.path.isfile(image_path):
        raise Http404('Image file not found')

    # Create a response that serves the image file
    response = FileResponse(open(image_path, 'rb'))
    response['Content-Type'] = 'image/jpeg'

    return response

# POST Methods


@api_view(['POST'])
def CreateProfile(request):
    fname = request.data.get('fname')
    lname = request.data.get('lname')
    bio = request.data.get('bio')
    uid = request.data.get('uid')

    parser_classes = (
        MultiPartParser,
        JSONParser,
    )

    file = request.data.get('avatar')
    url = cloudinary.uploader.upload(file)['secure_url']

    post = Profile.objects.create(firstName=fname, lastName=lname,
                                  username_id=uid, bio=bio, profile_picture=url, posts=[], likes=[])
    data = {
        'User ID': post.username_id,
        'First Name': post.firstName,
        'Last Name': post.lastName,
        'Bio': post.bio,
        'Avatar': post.profile_picture,
        'Posts': post.posts,
        'Likes': post.likes,
    }
    return Response(data)


@api_view(['POST'])
def CreatePost(request):
    author = request.data.get('id')
    caption = request.data.get('lname')

    parser_classes = (
        MultiPartParser,
        JSONParser,
    )

    file = request.data.get('image')
    url = cloudinary.uploader.upload(file)['secure_url']

    post = Post.objects.create(
        author_id=author, image=url, caption=caption, liked_by=[])
    data = {
        'User ID': post.author_id,
        'Image URL': post.image,
        'Caption': post.caption,
        'Date Created': post.created_at,
        'Liked By': post.liked_by
    }
    return Response(data)
