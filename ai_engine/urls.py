from django.urls import path
from .views import StudentPredictionView

urlpatterns = [
    path('predict/', StudentPredictionView.as_view()),
]