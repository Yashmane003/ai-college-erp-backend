from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from .models import Student
from .serializers import StudentSerializer

from rest_framework.permissions import IsAuthenticated
from accounts.permissions import IsAdmin, IsFaculty


class StudentListCreateView(APIView):

    permission_classes = [IsAuthenticated]

    def get(self, request):

        # 🎓 STUDENT → see only own data
        if request.user.role == 'student':
            students = Student.objects.filter(email=request.user.email)

        # 👨‍🏫 FACULTY + ADMIN → see all
        elif request.user.role in ['admin', 'faculty']:
            students = Student.objects.all()

        else:
            return Response({"error": "Unauthorized"}, status=403)

        serializer = StudentSerializer(students, many=True)
        return Response(serializer.data)


    def post(self, request):

        # 🔴 ONLY ADMIN CAN CREATE
        if request.user.role != 'admin':
            return Response(
                {"error": "Only admin can add students"},
                status=403
            )

        serializer = StudentSerializer(data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=201)

        return Response(serializer.errors, status=400)


class StudentDetailView(APIView):

    permission_classes = [IsAuthenticated]

    def get_object(self, pk):
        try:
            return Student.objects.get(pk=pk)
        except Student.DoesNotExist:
            return None

    def get(self, request, pk):
        student = self.get_object(pk)

        if not student:
            return Response({"error": "Not found"}, status=404)

        # 🎓 Student can only see own record
        if request.user.role == 'student' and student.email != request.user.email:
            return Response({"error": "Not allowed"}, status=403)

        serializer = StudentSerializer(student)
        return Response(serializer.data)

    def put(self, request, pk):
        student = self.get_object(pk)

        if not student:
            return Response({"error": "Not found"}, status=404)

        # 🔴 Only Admin can update
        if request.user.role != 'admin':
            return Response({"error": "Only admin allowed"}, status=403)

        serializer = StudentSerializer(student, data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)

        return Response(serializer.errors, status=400)

    def delete(self, request, pk):
        student = self.get_object(pk)

        if not student:
            return Response({"error": "Not found"}, status=404)

        # 🔴 Only Admin can delete
        if request.user.role != 'admin':
            return Response({"error": "Only admin allowed"}, status=403)

        student.delete()
        return Response({"message": "Deleted"})