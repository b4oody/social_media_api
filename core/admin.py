from django.contrib import admin
from core.models import (
    Profile,
    Post,
    Follower,
    Like,
    Commentary,
    Blocked
)

admin.site.register(Profile)
admin.site.register(Post)
admin.site.register(Follower)
admin.site.register(Like)
admin.site.register(Commentary)
admin.site.register(Blocked)
