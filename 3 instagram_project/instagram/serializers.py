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


class PostReadSerializer(serializers.ModelSerializer):
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


class PostWriteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = ["id", "user", "caption", "images"]

    images = serializers.ListField(
        child=serializers.ImageField(),
        write_only=True,
        required=False,
    )
    user = serializers.PrimaryKeyRelatedField(
        queryset=UserProfile.objects.all(), required=False
    )

    def validate(self, attrs):
        request = self.context.get("request")
        is_partial = request and request.method == "PATCH"

        if is_partial:
            # PATCH: if images key is provided, it must be non-empty
            if "images" in attrs and not attrs["images"]:
                raise serializers.ValidationError(
                    {"images": "A post must have at least one image."}
                )
        else:
            # POST / PUT: images is required and must be non-empty
            if not attrs.get("images"):
                raise serializers.ValidationError(
                    {"images": "A post must have at least one image."}
                )
        return attrs

    def create(self, validated_data):
        images = validated_data.pop("images", [])
        post = Post.objects.create(**validated_data)
        Image.objects.bulk_create([Image(post=post, image=img) for img in images])
        return post

    def update(self, instance, validated_data):
        images = validated_data.pop("images", None)
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()

        if images:
            instance.images.all().delete()
            Image.objects.bulk_create(
                [Image(post=instance, image=img) for img in images]
            )
        return instance

    def to_representation(self, instance):
        return PostReadSerializer(instance, context=self.context).data

    def to_internal_value(self, data):
        # Convert empty string to empty list for ListField
        if hasattr(data, "get") and data.get("images") == "":
            data = data.copy()
            data.setlist("images", [])
        return super().to_internal_value(data)
