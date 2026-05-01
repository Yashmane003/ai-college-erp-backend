from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from .models import Marks
from .serializers import MarksSerializer
from rest_framework.permissions import IsAuthenticated

class MarksListCreateView(APIView):

    permission_classes = [IsAuthenticated]

    def get(self, request):

        # 🎓 Student → only own marks
        if request.user.role == 'student':
            marks = Marks.objects.filter(student__email=request.user.email)

        # 👨‍🏫 Faculty + Admin → all marks
        elif request.user.role in ['admin', 'faculty']:
            marks = Marks.objects.all()

        else:
            return Response({"error": "Unauthorized"}, status=403)

        serializer = MarksSerializer(marks, many=True)
        return Response(serializer.data)


    def post(self, request):

        # 🔴 Only Admin + Faculty can add marks
        if request.user.role not in ['admin', 'faculty']:
            return Response(
                {"error": "Only faculty/admin can add marks"},
                status=403
            )

        serializer = MarksSerializer(data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=201)

        return Response(serializer.errors, status=400)


class MarksDetailView(APIView):

    permission_classes = [IsAuthenticated]

    def get_object(self, pk):
        try:
            return Marks.objects.get(pk=pk)
        except Marks.DoesNotExist:
            return None

    def get(self, request, pk):
        marks = self.get_object(pk)

        if not marks:
            return Response({"error": "Not found"}, status=404)

        # 🎓 Student → only own record
        if request.user.role == 'student' and marks.student.email != request.user.email:
            return Response({"error": "Not allowed"}, status=403)

        serializer = MarksSerializer(marks)
        return Response(serializer.data)

    def put(self, request, pk):
        marks = self.get_object(pk)

        if not marks:
            return Response({"error": "Not found"}, status=404)

        # 🔴 Only Admin + Faculty
        if request.user.role not in ['admin', 'faculty']:
            return Response({"error": "Not allowed"}, status=403)

        serializer = MarksSerializer(marks, data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)

        return Response(serializer.errors, status=400)

    def delete(self, request, pk):
        marks = self.get_object(pk)

        if not marks:
            return Response({"error": "Not found"}, status=404)

        # 🔴 Only Admin can delete
        if request.user.role != 'admin':
            return Response({"error": "Only admin allowed"}, status=403)

        marks.delete()
        return Response({"message": "Deleted successfully"})
    