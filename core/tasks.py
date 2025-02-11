from celery import shared_task
from core.models import Post
from django.utils import timezone

from user.models import User


@shared_task
def create_post(owner_id, title, body, schedule_time=None):
    if schedule_time:
        schedule_time = timezone.make_aware(schedule_time)
    else:
        schedule_time = timezone.now()

    owner = User.objects.get(id=owner_id)
    post = Post.objects.create(
        title=title,
        body=body,
        owner=owner,
        created_at=schedule_time,
    )
    return f"Post '{post.title}' created at {post.created_at}"
