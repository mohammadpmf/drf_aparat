from django.urls import path, include
from rest_framework.routers import DefaultRouter

from .views import UserProfileViewSet, PostViewSet

router = DefaultRouter()
router.register("profiles", UserProfileViewSet, basename="user-profiles")
router.register("posts", PostViewSet, basename="posts")
urlpatterns = router.urls


# instagram/profiles/
# instagram/profile/me
# instagram/posts/
