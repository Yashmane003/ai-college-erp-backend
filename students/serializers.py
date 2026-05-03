from django.contrib.auth import get_user_model
from rest_framework import serializers

from .models import Student

User = get_user_model()


class StudentSerializer(serializers.ModelSerializer):

    # 🔐 Write-only password (used to create/update login account)
    password = serializers.CharField(write_only=True, required=False, min_length=6)

    class Meta:
        model = Student
        fields = ('id', 'name', 'email', 'department', 'year', 'password')

    def create(self, validated_data):
        password = validated_data.pop('password', None)

        if not password:
            raise serializers.ValidationError({'password': 'This field is required.'})

        student = Student.objects.create(**validated_data)

        User.objects.create_user(
            username=student.email,
            email=student.email,
            password=password,
            role='student',
        )

        return student

    def update(self, instance, validated_data):
        password = validated_data.pop('password', None)
        old_email = instance.email

        student = super().update(instance, validated_data)

        user = User.objects.filter(email=old_email, role='student').first()

        if user:
            user.username = student.email
            user.email = student.email

            if password:
                user.set_password(password)

            user.save()

        return student
