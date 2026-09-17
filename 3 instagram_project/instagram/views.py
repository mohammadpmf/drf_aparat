from django.shortcuts import render
from rest_framework.viewsets import ModelViewSet
from django.db.models import Prefetch
from drf_spectacular.utils import extend_schema, extend_schema_view
from rest_framework.parsers import MultiPartParser, FormParser, JSONParser

from .models import UserProfile, Post, Comment
from .serializers import (
    UserProfileSerializer,
    PostReadSerializer,
    PostWriteSerializer,
)


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


def _post_multipart_schema(required_user: bool = True):
    schema = {
        "multipart/form-data": {
            "type": "object",
            "properties": {
                "user": {"type": "integer"},
                "caption": {"type": "string"},
                "images": {
                    "type": "array",
                    "items": {"type": "string", "format": "binary"},
                },
            },
        }
    }
    if required_user:
        schema["multipart/form-data"]["required"] = ["user"]
    return schema


@extend_schema_view(
    create=extend_schema(request=_post_multipart_schema(required_user=True)),
    update=extend_schema(request=_post_multipart_schema(required_user=True)),
    partial_update=extend_schema(request=_post_multipart_schema(required_user=False)),
)
class PostViewSet(ModelViewSet):
    parser_classes = [MultiPartParser, FormParser, JSONParser]

    def get_serializer_class(self):
        if self.action in ("create", "update", "partial_update"):
            return PostWriteSerializer
        return PostReadSerializer

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
