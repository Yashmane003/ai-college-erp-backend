from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):

    ROLE_CHOICES = (
        ('admin', 'Admin'),
        ('faculty', 'Faculty'),
        ('student', 'Student'),
    )

    role = models.CharField(max_length=10, choices=ROLE_CHOICES, default='student')

    def save(self, *args, **kwargs):

        # If superuser → admin role
        if self.is_superuser:
            self.role = 'admin'

        # 🔥 Restrict multiple admins
        if self.role == 'admin':
            existing_admin = User.objects.filter(role='admin').exclude(pk=self.pk)

            if existing_admin.exists():
                raise ValueError("Only one admin is allowed")

        super().save(*args, **kwargs)