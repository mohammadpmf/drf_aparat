from django.shortcuts import render
from rest_framework.viewsets import ModelViewSet
from django.db.models import Prefetch
from drf_spectacular.utils import extend_schema, extend_schema_view

from .models import UserProfile, Post, Comment, Image
from .serializers import UserProfileSerializer, PostSerializer


@extend_schema_view(
    list=extend_schema(
        summary="User List",
        description="Returns a list of all users",
        responses={200: UserProfileSerializer(many=True)},
    ),
    retrieve=extend_schema(
        summary="Retrieve a user",
        responses={200: UserProfileSerializer},
    ),
    create=extend_schema(
        summary="Create a user",
        request=UserProfileSerializer,
        responses={201: UserProfileSerializer},
    ),
    update=extend_schema(
        summary="Update a user",
        request=UserProfileSerializer,
        responses={200: UserProfileSerializer},
    ),
    partial_update=extend_schema(
        summary="Partially update a user",
        request=UserProfileSerializer,
        responses={200: UserProfileSerializer},
    ),
    destroy=extend_schema(
        summary="Delete a user",
        responses={204: None},
    ),
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
