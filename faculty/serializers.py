from django.contrib.auth import get_user_model
from rest_framework import serializers

from .models import Faculty, Subject

User = get_user_model()


class FacultySerializer(serializers.ModelSerializer):

    # 🔐 Write-only password (used to create/update login account)
    password = serializers.CharField(write_only=True, required=False, min_length=6)

    class Meta:
        model = Faculty
        fields = ('id', 'name', 'email', 'department', 'designation', 'password')

    def create(self, validated_data):
        password = validated_data.pop('password', None)

        if not password:
            raise serializers.ValidationError({'password': 'This field is required.'})

        faculty = Faculty.objects.create(**validated_data)

        User.objects.create_user(
            username=faculty.email,
            email=faculty.email,
            password=password,
            role='faculty',
        )

        return faculty

    def update(self, instance, validated_data):
        password = validated_data.pop('password', None)
        old_email = instance.email

        faculty = super().update(instance, validated_data)

        user = User.objects.filter(email=old_email, role='faculty').first()

        if user:
            user.username = faculty.email
            user.email = faculty.email

            if password:
                user.set_password(password)

            user.save()

        return faculty


class SubjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = Subject
        fields = '__all__'
