from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from materials.models import Course, Lesson
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

