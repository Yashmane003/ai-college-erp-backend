from django.db import models
from students.models import Student
from faculty.models import Subject


class Attendance(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE)
    percentage = models.FloatField()

    def __str__(self):
        return self.student.name