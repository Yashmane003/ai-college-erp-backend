from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

from .models import TimetableEntry
from .serializers import TimetableEntrySerializer

import random


class GenerateTimetableView(APIView):

    permission_classes = [IsAuthenticated]

    # 🟢 GET → Everyone can view timetable
    def get(self, request):

        timetable = TimetableEntry.objects.all()
        serializer = TimetableEntrySerializer(timetable, many=True)

        return Response(serializer.data)


    # 🔴 POST → Only Admin generates timetable
    def post(self, request):

        if request.user.role != 'admin':
            return Response(
                {"error": "Only admin can generate timetable"},
                status=403
            )

        subjects = request.data.get('subjects', [])
        faculty = request.data.get('faculty', [])
        rooms = request.data.get('rooms', [])

        if not subjects or not faculty or not rooms:
            return Response(
                {"error": "subjects, faculty, rooms required"},
                status=400
            )

        days = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday"]
        time_slots = ["10:00", "11:00", "12:00", "2:00", "3:00"]

        random.shuffle(subjects)
        random.shuffle(faculty)
        random.shuffle(rooms)

        # 🔥 Clear old timetable before generating new
        TimetableEntry.objects.all().delete()

        timetable = []

        subject_index = 0
        faculty_index = 0
        room_index = 0

        for day in days:
            for time in time_slots:

                if subject_index >= len(subjects):
                    subject_index = 0

                if faculty_index >= len(faculty):
                    faculty_index = 0

                if room_index >= len(rooms):
                    room_index = 0

                entry = TimetableEntry.objects.create(
                    day=day,
                    time_slot=time,
                    subject=subjects[subject_index],
                    faculty=faculty[faculty_index],
                    room=rooms[room_index]
                )

                timetable.append(entry)

                subject_index += 1
                faculty_index += 1
                room_index += 1

        serializer = TimetableEntrySerializer(timetable, many=True)
        return Response(serializer.data)