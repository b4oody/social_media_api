from rest_framework import serializers

from core.models import (
    Profile,
    Post,
    Follower,
    Like,
    Commentary,
    Blocked
)


class RetrieveProfileSerializer(serializers.ModelSerializer):
    username = serializers.ReadOnlyField(source="user.username")
    following = serializers.IntegerField(read_only=True)
    followers = serializers.IntegerField(read_only=True)

    class Meta:
        model = Profile
        fields = [
            "id",
            "user",
            "username",
            "following",
            "followers",
            "description",
            "privacy_setting",
        ]


class PostSerializer(serializers.ModelSerializer):
    owner = serializers.ReadOnlyField(source="owner.username")

    class Meta:
        model = Post
        fields = ["id", "title", "owner", "created_at"]


class PostRetrieveSerializer(PostSerializer):
    class Meta:
        model = Post
        fields = PostSerializer.Meta.fields + ["body"]


class LikesListPostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Like
        fields = ["id", "user"]


class LikeCreatePostSerializer(LikesListPostSerializer):
    class Meta:
        model = Like
        fields = LikesListPostSerializer.Meta.fields + ["post"]
