from celery import shared_task
from django.utils import timezone

from users.models import User


@shared_task
def block_user():
    """Функция по блокированию пользователя, если он не заходил более 30 дней."""

    active_users = User.objects.filter(is_active=True)
    for user in active_users:
        if user.last_login.date() < timezone.now().date() - timezone.timedelta(days=30):
            user.is_active = False
            user.save()