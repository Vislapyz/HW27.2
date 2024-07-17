from rest_framework import serializers
from rest_framework.fields import SerializerMethodField

from materials.models import Course, Lesson, SubscriptionCourse
from materials.validators import LinkValidator


class CourseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Course
        fields = "__all__"


class LessonSerializer(serializers.ModelSerializer):
    class Meta:
        model = Lesson
        fields = "__all__"
        validators = [LinkValidator(field='link')]


class CourseDetailSerializer(serializers.ModelSerializer):
    count_lessons_for_course = SerializerMethodField()
    lessons = LessonSerializer(many=True, read_only=True)
    subscription = SerializerMethodField(read_only=True)

    class Meta:
        model = Course
        fields = "__all__"

    def get_is_subscription(self, course):
        return SubscriptionCourse.objects.filter(course=course, user=self.context['request'].user).exists()

    @staticmethod
    def get_count_lessons_for_course(course):
        return course.lessons.count()


class SubscriptionCourseSerializer(serializers.ModelSerializer):
    class Meta:
        model = SubscriptionCourse
        fields = "__all__"