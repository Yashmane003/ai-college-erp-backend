from django.urls import path
from .views import AttendanceListCreateView, AttendanceDetailView

urlpatterns = [
    path('attendance/', AttendanceListCreateView.as_view()),
    path('attendance/<int:pk>/', AttendanceDetailView.as_view()),
]