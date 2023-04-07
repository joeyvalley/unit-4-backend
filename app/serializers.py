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


class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = '__all__'


class PostSerializer(serializers.ModelSerializer):
    author = UserSerializer()

    class Meta:
        model = Post
        fields = '__all__'


class ProfileSerializer(serializers.ModelSerializer):

    class Meta:
        model = Profile
        fields = '__all__'


# class FollowSerializer(serializers.ModelSerializer):

#     class Meta:
#         model = Follow
#         fields = '__all__'
