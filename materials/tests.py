from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from materials.models import Course, Lesson, SubscriptionCourse
from users.models import User


class LessonTestCase(APITestCase):
    def setUp(self):
        self.user = User.objects.create(email="test@test.ru")
        self.course = Course.objects.create(
            name_course="Test Course", description="Test Course"
        )
        self.lesson = Lesson.objects.create(
            name_ln="Test Lesson",
            description="Test Lesson",
            link_video="https://www.youtube.com/",
            name_course=self.course,
            owner=self.user,
        )
        self.client.force_authenticate(user=self.user)

    def test_lesson_retrieve(self):
        url = reverse("materials:lesson-get", args=(self.lesson.pk,))
        response = self.client.get(url)
        data = response.json()
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(data.get("name_ln"), self.lesson.name_ln)
        self.assertEqual(data.get("name_course"), self.lesson.name_course.pk)

    def test_lesson_create(self):
        url = reverse("materials:lesson-create")
        data = {
            "name_ln": "Test Lesson",
            "description": "Test Lesson",
            "link_video": "https://www.youtube.com/",
            "name_course": self.course.pk,
        }
        response = self.client.post(url, data)
        print(response.json())
        # self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Lesson.objects.all().count(), 1)

    def test_lesson_update(self):
        url = reverse("materials:lesson-update", args=(self.lesson.pk,))
        data = {"name_ln": "Updated Test Lesson"}
        response = self.client.put(url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(Lesson.objects.get(pk=self.lesson.pk).name_ln, "Updated Test Lesson")

    def test_lesson_delete(self):
        url = reverse("materials:lesson-delete", args=(self.lesson.pk,))
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Lesson.objects.all().count(), 0)

    def test_lesson_list(self):
        url = reverse("materials:lesson-list")
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.json()["results"]), 1)

class SubscriptionTestCase(APITestCase):

    def setUp(self):
        self.user = User.objects.create(email="test@test.ru")
        self.course = Course.objects.create(
            name_course="Test Course", description="Test Course"
        )
        self.client.force_authenticate(user=self.user)
        self.url = reverse("materials:subscription")

    def test_subscription_create(self):
        data = {"user": self.user.pk, "course": self.course.pk}
        response = self.client.post(self.url, data)
        temp_data = response.json()
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(temp_data.get("message"), "подписка добавлена")
        self.assertEqual(SubscriptionCourse.objects.all().count(), 1)

    def test_subscribe_delete(self):
        SubscriptionCourse.objects.create(user=self.user, course=self.course)
        data = {
            "user": self.user.id,
            "course": self.course.id,
        }
        response = self.client.post(self.url, data=data)
        temp_data = response.json()
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(temp_data.get("message"), "подписка удалена")
        self.assertEqual(SubscriptionCourse.objects.all().count(), 0)






