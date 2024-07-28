from celery import shared_task
from django.core.mail import send_mail
from django.conf import settings
from materials.models import SubscriptionCourse, Course


@shared_task
def send_message_update_course(course_id):
    course = Course.objects.get(pk=course_id)
    course_users = SubscriptionCourse.objects.filter(course=course_id)
    email_list = []
    for user in course_users:
        email_list.append(user.email)
    if email_list:
        send_mail(
            subject=f"Обновление по курсу {course.name_course}",
            message=f"Вы подписаны на обновления курса, вышла новая информация по курсу.",
            from_email=settings.EMAIL_HOST_USER,
            recipient_list=email_list,
            fail_silently=True
        )