from django.db import models
from students.models import Student


class Marks(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    assignment_score = models.FloatField()
    midterm_score = models.FloatField()
    final_score = models.FloatField(null=True, blank=True)

    def __str__(self):
        return self.student.name