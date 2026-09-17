from django.shortcuts import render
from rest_framework.viewsets import ModelViewSet
from django.db.models import Prefetch
from drf_spectacular.utils import extend_schema

from .models import UserProfile, Post, Comment, Image
from .serializers import UserProfileSerializer, PostSerializer


@extend_schema(
    summary="User List",
    description="Returns a list of all users",
    responses={200: UserProfileSerializer(many=True)},
)
class UserProfileViewSet(ModelViewSet):
    serializer_class = UserProfileSerializer
    queryset = UserProfile.objects.filter(is_active=True).select_related("user")


class PostViewSet(ModelViewSet):
    serializer_class = PostSerializer

    def get_queryset(self):
        comments_qs = Comment.objects.select_related("user__user")
        likes_qs = UserProfile.objects.select_related("user")
        q = (
            Post.objects.filter(is_active=True)
            .select_related("user__user")
            .prefetch_related(
                "images",
                Prefetch("comments", queryset=comments_qs),
                Prefetch("likes", queryset=likes_qs),
            )
        )
        return q
