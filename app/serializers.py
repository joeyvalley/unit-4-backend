from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Comment, Post, Profile


class UserSerializer(serializers.ModelSerializer):
    profile = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = ('id', 'username', 'email', 'password', 'profile')
        extra_kwargs = {
            'password': {
                'write_only': True
            }
        }

    def get_profile(self, obj):
        profile = Profile.objects.filter(username=obj).first()
        return ProfileSerializer(profile).data

    def __str__(self):
        return str(self.profile)


class CommentSerializer(serializers.ModelSerializer):
    user = UserSerializer()

    class Meta:
        model = Comment
        fields = ('text', 'user')


class PostSerializer(serializers.ModelSerializer):
    author = UserSerializer()
    comments = CommentSerializer(many=True, read_only=True)

    class Meta:
        model = Post
        fields = '__all__'


class ProfileSerializer(serializers.ModelSerializer):

    class Meta:
        model = Profile
        fields = '__all__'
