from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from .models import Attendance
from .serializers import AttendanceSerializer
from rest_framework.permissions import IsAuthenticated

class AttendanceListCreateView(APIView):

    permission_classes = [IsAuthenticated]

    def get(self, request):

        # 🎓 Student → only own attendance
        if request.user.role == 'student':
            attendance = Attendance.objects.filter(student__email=request.user.email)

        # 👨‍🏫 Faculty + Admin → all attendance
        elif request.user.role in ['admin', 'faculty']:
            attendance = Attendance.objects.all()

        else:
            return Response({"error": "Unauthorized"}, status=403)

        serializer = AttendanceSerializer(attendance, many=True)
        return Response(serializer.data)


    def post(self, request):

        # 🔴 Only Faculty + Admin can add attendance
        if request.user.role not in ['admin', 'faculty']:
            return Response(
                {"error": "Only faculty/admin allowed"},
                status=403
            )

        serializer = AttendanceSerializer(data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=201)

        return Response(serializer.errors, status=400)


class AttendanceDetailView(APIView):

    permission_classes = [IsAuthenticated]

    def get_object(self, pk):
        try:
            return Attendance.objects.get(pk=pk)
        except Attendance.DoesNotExist:
            return None

    def get(self, request, pk):
        attendance = self.get_object(pk)

        if not attendance:
            return Response({"error": "Not found"}, status=404)

        # 🎓 Student → only own record
        if request.user.role == 'student' and attendance.student.email != request.user.email:
            return Response({"error": "Not allowed"}, status=403)

        serializer = AttendanceSerializer(attendance)
        return Response(serializer.data)

    def put(self, request, pk):
        attendance = self.get_object(pk)

        if not attendance:
            return Response({"error": "Not found"}, status=404)

        # 🔴 Only Faculty + Admin
        if request.user.role not in ['admin', 'faculty']:
            return Response({"error": "Not allowed"}, status=403)

        serializer = AttendanceSerializer(attendance, data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)

        return Response(serializer.errors, status=400)

    def delete(self, request, pk):
        attendance = self.get_object(pk)

        if not attendance:
            return Response({"error": "Not found"}, status=404)

        # 🔴 Only Admin
        if request.user.role != 'admin':
            return Response({"error": "Only admin allowed"}, status=403)

        attendance.delete()
        return Response({"message": "Deleted successfully"})
