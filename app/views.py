
# Models and serializers for admin panel.
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.authtoken.models import Token
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework import status
from rest_framework_simplejwt.views import TokenObtainPairView, TokenVerifyView
from rest_framework.views import APIView
import cloudinary.uploader
from rest_framework.parsers import MultiPartParser, JSONParser
from django.http import Http404, FileResponse
from django.conf import settings
import os
import jwt
from .models import Comment, Post, Profile
from .serializers import CommentSerializer, PostSerializer, ProfileSerializer, UserSerializer

# Dependencies for Django authorization/authentication.
from django.contrib.auth.models import User
from rest_framework import permissions, viewsets
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
    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS or request.method == 'PUT':
            return True
        return obj.owner == request.user


class IsStaffOrTargetUser(permissions.BasePermission):
    def has_permission(self, request, view):
        return view.action == 'retrieve' or request.user.is_staff

    def has_object_permission(self, request, view, obj):
        return obj == request.user or request.user.is_staff


# JWT authorization / authentication views
class CustomTokenObtainPairView(TokenObtainPairView):
    def dotheThing():
        return Response({"hi": "bitch"})


class CustomTokenVerifyView(TokenVerifyView):
    def decode_token(self, token):
        try:
            decoded_token = jwt.decode(
                token, settings.SECRET_KEY, algorithms=['HS256'])
            return decoded_token
        except jwt.ExpiredSignatureError:
            raise exceptions.AuthenticationFailed('Token has expired')
        except jwt.InvalidTokenError:
            raise exceptions.AuthenticationFailed('Token is invalid')

    def post(self, request, *args, **kwargs):
        token = request.data['token']
        try:
            decoded_token = self.decode_token(token)
            print(f"Decoded token: {decoded_token}")
            return Response({'token': token, 'user_id': decoded_token['user_id']})
        except Exception as e:
            return Response(False)

        return Response({'detail': 'Your custom success message.'}, status=status.HTTP_200_OK)


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


@api_view(['POST'])
def like(request):
    post_id = request.data['post_id']
    post = Post.objects.get(id=post_id)
    user_id = request.data['user_id']
    if user_id in post.liked_by:
        post.liked_by.remove(user_id)
        post.save()
        print("removed like")
        return Response({'current like': post.liked_by})
    post.liked_by.append(user_id)
    post.save()
    print()
    return Response({'current like': post.liked_by})


class CustomAuthToken(ObtainAuthToken):
    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data,
                                           context={'request': request})
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        token, created = Token.objects.get_or_create(user=user)
        print(token)
        return Response({'token': token.key, 'username': request.data['username']})


class MyView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request):
        print("geelo")
        # token = request.data.get('token')
        # print()
        # return Response(token)


@api_view(['POST'])
def dislike(request):
    post_id = request.data['post_id']
    post = Post.objects.get(id=post_id)
    user_id = request.data['user_id']
    if user_id in post.disliked_by:
        post.disliked_by.remove(user_id)
        post.save()
        print("Hate it")
        return Response({'Dislikes': post.dislike_by})
    post.dislike_by.append(user_id)
    post.save()
    print('Hated it')
    return Response({'current dislike': post.dislike_by})
