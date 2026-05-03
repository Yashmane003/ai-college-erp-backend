from django.contrib.auth import get_user_model
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from .models import Faculty, Subject

User = get_user_model()
from .serializers import FacultySerializer, SubjectSerializer

from rest_framework.permissions import IsAuthenticated

class FacultyListCreateView(APIView):

    permission_classes = [IsAuthenticated]

    def get(self, request):

        # 👨‍🏫 Faculty + Admin → can view
        if request.user.role in ['admin', 'faculty']:
            faculty = Faculty.objects.all()

        # 🎓 Student → not allowed
        else:
            return Response({"error": "Not allowed"}, status=403)

        serializer = FacultySerializer(faculty, many=True)
        return Response(serializer.data)


    def post(self, request):

        # 🔴 Only Admin can create
        if request.user.role != 'admin':
            return Response({"error": "Only admin allowed"}, status=403)

        serializer = FacultySerializer(data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=201)

        return Response(serializer.errors, status=400)
    
class FacultyDetailView(APIView):

    permission_classes = [IsAuthenticated]

    def get_object(self, pk):
        try:
            return Faculty.objects.get(pk=pk)
        except Faculty.DoesNotExist:
            return None
        
    def get(self, request, pk):

        # 👨‍🏫 Admin + Faculty → allowed
        if request.user.role not in ['admin', 'faculty']:
            return Response({"error": "Not allowed"}, status=403)

        faculty = self.get_object(pk)

        if not faculty:
            return Response({"error": "Not found"}, status=404)

        serializer = FacultySerializer(faculty)
        return Response(serializer.data)


    def put(self, request, pk):

        # 🔴 Only Admin
        if request.user.role != 'admin':
            return Response({"error": "Only admin allowed"}, status=403)

        faculty = self.get_object(pk)

        if not faculty:
            return Response({"error": "Not found"}, status=404)

        serializer = FacultySerializer(faculty, data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)

        return Response(serializer.errors, status=400)


    def delete(self, request, pk):

        # 🔴 Only Admin
        if request.user.role != 'admin':
            return Response({"error": "Only admin allowed"}, status=403)

        faculty = self.get_object(pk)

        if not faculty:
            return Response({"error": "Not found"}, status=404)

        # 🧹 Also remove linked login account
        User.objects.filter(email=faculty.email, role='faculty').delete()

        faculty.delete()
        return Response({"message": "Deleted successfully"})

# subject views   
class SubjectListCreateView(APIView):

    permission_classes = [IsAuthenticated]

    def get(self, request):

        # ✅ Everyone can view (Admin, Faculty, Student)
        subjects = Subject.objects.all()

        serializer = SubjectSerializer(subjects, many=True)
        return Response(serializer.data)


    def post(self, request):

        # 🔴 Only Admin can create subject
        if request.user.role != 'admin':
            return Response({"error": "Only admin allowed"}, status=403)

        serializer = SubjectSerializer(data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=201)

        return Response(serializer.errors, status=400)
    
class SubjectDetailView(APIView):

    permission_classes = [IsAuthenticated]

    def get_object(self, pk):
        try:
            return Subject.objects.get(pk=pk)
        except Subject.DoesNotExist:
            return None
    
    def get(self, request, pk):

        # ✅ All roles can view
        subject = self.get_object(pk)

        if not subject:
            return Response({"error": "Not found"}, status=404)

        serializer = SubjectSerializer(subject)
        return Response(serializer.data)


    def put(self, request, pk):

        # 🔴 Only Admin
        if request.user.role != 'admin':
            return Response({"error": "Only admin allowed"}, status=403)

        subject = self.get_object(pk)

        if not subject:
            return Response({"error": "Not found"}, status=404)

        serializer = SubjectSerializer(subject, data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)

        return Response(serializer.errors, status=400)


    def delete(self, request, pk):

        # 🔴 Only Admin
        if request.user.role != 'admin':
            return Response({"error": "Only admin allowed"}, status=403)

        subject = self.get_object(pk)

        if not subject:
            return Response({"error": "Not found"}, status=404)

        subject.delete()
        return Response({"message": "Deleted successfully"})