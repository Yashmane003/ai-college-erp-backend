from django.db import models


class Room(models.Model):
    room_number = models.CharField(max_length=20)
    capacity = models.IntegerField()

    def __str__(self):
        return self.room_number

class TimetableEntry(models.Model):
    day = models.CharField(max_length=20)
    time_slot = models.CharField(max_length=20)
    subject = models.CharField(max_length=100)
    faculty = models.CharField(max_length=100)
    room = models.CharField(max_length=20)

    def __str__(self):
        return self.day