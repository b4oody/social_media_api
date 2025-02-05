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
