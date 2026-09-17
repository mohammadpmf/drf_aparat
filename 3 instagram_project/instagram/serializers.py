from django.conf import settings
from rest_framework import serializers

from .models import UserProfile, Post, Image, Comment


class BriefUserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields = [
            "id",
            "profile_username",
            "profile_picture",
        ]

    id = serializers.IntegerField(source="user.id")
    profile_username = serializers.CharField(source="username")


class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields = [
            "first_name",
            "last_name",
            "email",
            "bio",
            "profile_picture",
            "username",
            "profile_username",
        ]

    first_name = serializers.CharField(source="user.first_name")
    last_name = serializers.CharField(source="user.last_name")
    email = serializers.CharField(source="user.email")
    username = serializers.CharField(source="user.username")
    profile_username = serializers.CharField(source="username")


class ImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Image
        fields = [
            "id",
            "image",
        ]


class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = [
            "id",
            "text",
            "user",
        ]

    user = BriefUserProfileSerializer()


class PostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = [
            "id",
            "user",
            "caption",
            "likes_count",
            "likes",
            "images",
            "comments",
        ]

    user = UserProfileSerializer()
    likes_count = serializers.SerializerMethodField()
    likes = BriefUserProfileSerializer(many=True)
    images = ImageSerializer(many=True)
    comments = CommentSerializer(many=True)

    def get_likes_count(self, instance: Post):
        return instance.likes.count()
