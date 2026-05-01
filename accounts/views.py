from rest_framework.views import APIView
from rest_framework.response import Response
from django.contrib.auth import authenticate
from rest_framework import status

from rest_framework.permissions import AllowAny
from rest_framework_simplejwt.tokens import RefreshToken


class LoginView(APIView):

    # ✅ Allow anyone (no authentication required)
    permission_classes = [AllowAny]

    def post(self, request):
        username = request.data.get("username")
        password = request.data.get("password")

        user = authenticate(username=username, password=password)

        if user:
            refresh = RefreshToken.for_user(user)

            return Response({
                "access": str(refresh.access_token),
                "refresh": str(refresh),
                "role": user.role,
                "username": user.username
            })

        return Response({"error": "Invalid credentials"}, status=401)