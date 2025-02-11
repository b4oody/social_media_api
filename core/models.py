import os
import uuid

from django.db import models
from django.utils.text import slugify

from social_media_api.settings.base import AUTH_USER_MODEL


def create_custom_path(instance, filename, path_prefix):
    _, extension = os.path.splitext(filename)
    return os.path.join(
        path_prefix,
        f"{slugify(str(instance))}-{uuid.uuid4()}{extension}"
    )


def profile_image_path(instance, filename):
    return create_custom_path(instance, filename, "uploads/profile_images/")


class Profile(models.Model):
    class PrivacySettings(models.TextChoices):
        PUBLIC = "public"
        PRIVATE = "private"

    user = models.OneToOneField(AUTH_USER_MODEL, on_delete=models.CASCADE)
    description = models.TextField(blank=True, null=True)
    image_profile = models.ImageField(
        upload_to=profile_image_path,
        blank=True,
        null=True,
        default="static/default_image/default_profile.png",
    )
    created_at = models.DateTimeField(auto_now_add=True)
    privacy_setting = models.CharField(
        max_length=10,
        choices=PrivacySettings,
        default=PrivacySettings.PUBLIC,
    )

    class Meta:
        indexes = [
            models.Index(fields=["user"]),
        ]

    def __str__(self):
        return f"Profile of {self.user}"


def post_image_path(instance, filename):
    return create_custom_path(instance, filename, "uploads/posts_images/")


class Post(models.Model):
    title = models.CharField(max_length=255)
    body = models.TextField()
    owner = models.ForeignKey(
        AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="posts"
    )
    created_at = models.DateTimeField(auto_now_add=True)

    image_post = models.ImageField(
        upload_to=post_image_path,
        blank=True,
        null=True
    )

    class Meta:
        indexes = [
            models.Index(fields=["owner"]),
            models.Index(fields=["created_at"]),
        ]
        ordering = ["-created_at"]

    def __str__(self):
        return self.title


class Follower(models.Model):
    follower = models.ForeignKey(
        AUTH_USER_MODEL,
        related_name="following",
        on_delete=models.CASCADE
    )
    following = models.ForeignKey(
        AUTH_USER_MODEL,
        related_name="followers",
        on_delete=models.CASCADE
    )
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ("follower", "following")
        indexes = [
            models.Index(fields=["follower", "following"]),
            models.Index(fields=["created_at"]),
        ]
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.follower} follows {self.following}"


class Like(models.Model):
    user = models.ForeignKey(
        AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="likes"
    )
    post = models.ForeignKey(
        Post,
        on_delete=models.CASCADE,
        related_name="likes"
    )
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ("user", "post")
        indexes = [
            models.Index(fields=["user"]),
            models.Index(fields=["post"]),
        ]
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.user} liked post {self.post.title}"


class Commentary(models.Model):
    user = models.ForeignKey(
        AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="commentaries"
    )
    post = models.ForeignKey(
        Post,
        on_delete=models.CASCADE,
        related_name="commentaries"
    )
    body = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        indexes = [
            models.Index(fields=["post"]),
            models.Index(fields=["user"]),
        ]
        ordering = ["-created_at"]

    def __str__(self):
        return f"Comment by {self.user} on post {self.post.title}"


class Blocked(models.Model):
    blocker = models.ForeignKey(
        AUTH_USER_MODEL,
        related_name="blocked_users",
        on_delete=models.CASCADE
    )
    blocked = models.ForeignKey(
        AUTH_USER_MODEL,
        related_name="blocked_by",
        on_delete=models.CASCADE
    )
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ("blocker", "blocked")
        indexes = [
            models.Index(fields=["blocker"]),
            models.Index(fields=["blocked"]),
        ]
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.blocker} blocked {self.blocked}"
