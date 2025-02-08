from rest_framework import permissions

from core.models import Blocked, Profile, Follower


class IsOwnerOrReadOnly(permissions.BasePermission):
    """
    Custom permission to only allow owners of a post to edit or delete it.
    """

    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True

        return obj.owner == request.user


class CanViewPostPermission(permissions.BasePermission):
    """
    Пермішн для перевірки, чи може користувач бачити пост.
    """

    def has_permission(self, request, view):
        if not request.user.is_authenticated:
            return False

        post = view.get_object()

        if Blocked.objects.filter(blocker=request.user, blocked=post.owner).exists():
            return False

        if post.owner.profile.privacy_setting == Profile.PrivacySettings.PRIVATE:
            if not post.owner in Follower.objects.filter(
                    follower=request.user
            ).values_list("following", flat=True):
                return False

        return True


class CanLikePostPermission(permissions.BasePermission):
    """
    Пермішн для перевірки, чи може користувач лайкати пост.
    """

    def has_permission(self, request, view):
        if not request.user.is_authenticated:
            return False

        post = view.get_object()

        if Blocked.objects.filter(blocker=request.user, blocked=post.owner).exists():
            return False

        if post.owner.profile.privacy_setting == Profile.PrivacySettings.PRIVATE:
            if not post.owner in Follower.objects.filter(
                    follower=request.user
            ).values_list("following", flat=True):
                return False

        return True


class CanCommentOnPostPermission(permissions.BasePermission):
    """
    Пермішн для перевірки, чи може користувач коментувати пост.
    """

    def has_permission(self, request, view):
        if not request.user.is_authenticated:
            return False

        post = view.get_object()

        if Blocked.objects.filter(blocker=request.user, blocked=post.owner).exists():
            return False

        if post.owner.profile.privacy_setting == Profile.PrivacySettings.PRIVATE:
            if not post.owner in Follower.objects.filter(
                    follower=request.user
            ).values_list("following", flat=True):
                return False

        return True
