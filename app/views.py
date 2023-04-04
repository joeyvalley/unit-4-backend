
# Models and serializers for admin panel.
from .models import Comment, Post, Profile
from .serializers import CommentSerializer, PostSerializer, ProfileSerializer, UserSerializer

# Dependencies for Django authorization/authentication.
from django.contrib.auth.models import User
from rest_framework import permissions, viewsets
from rest_framework.permissions import IsAuthenticated
from django.contrib.auth.hashers import make_password

# Dependencies for client views
from rest_framework.response import Response
from rest_framework.decorators import api_view


# Admin panel views and serializers.


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


@api_view(['GET'])
def mainFeed(request):
    posts = Post.objects.all()
    serializer = PostSerializer(posts, many=True)
    print(serializer.data)
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
