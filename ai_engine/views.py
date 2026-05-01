import pickle
import os

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated


BASE_DIR = os.path.dirname(os.path.abspath(__file__))
MODEL_PATH = os.path.join(BASE_DIR, 'student_model.pkl')

with open(MODEL_PATH, 'rb') as file:
    model = pickle.load(file)


class StudentPredictionView(APIView):

    # 🔐 Require login (JWT)
    permission_classes = [IsAuthenticated]

    def post(self, request):

        # (Optional safety check)
        if request.user.role not in ['admin', 'faculty', 'student']:
            return Response({"error": "Unauthorized"}, status=403)

        attendance = request.data.get('attendance')
        assignment = request.data.get('assignment_score')
        midterm = request.data.get('midterm_score')

        # ⚠️ Input validation (important improvement)
        if attendance is None or assignment is None or midterm is None:
            return Response(
                {"error": "attendance, assignment_score, midterm_score required"},
                status=400
            )

        prediction = model.predict([[attendance, assignment, midterm]])
        final_score = round(prediction[0], 2)

        if final_score >= 75:
            risk = "Low"
        elif final_score >= 50:
            risk = "Medium"
        else:
            risk = "High"

        return Response({
            "predicted_final_score": final_score,
            "risk_level": risk
        })