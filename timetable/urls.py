from django.urls import path
from .views import GenerateTimetableView

urlpatterns = [
    path('generate-timetable/', GenerateTimetableView.as_view()),
]