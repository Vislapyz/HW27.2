from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from materials.models import Course, Lesson
from users.models import User


class LessonTestCase(APITestCase):
    def setUp(self):
        self.user = User.objects.create(email="test@test.ru")
        self.course = Course.objects.create(
            name_course="Test Course", description="Test Course", owner=self.user
        )
        self.lesson = Lesson.objects.create(
            name_ln="Test Lesson",
            description="Test Lesson",
            link_video="https://www.youtube.com/",
            owner=self.user,
            name_course=self.course,
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
            "name_ln": "Test1",
            "description": "Test1",
            "link_video": "https://www.youtube.com/",
            "name_course": self.course.pk,
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
