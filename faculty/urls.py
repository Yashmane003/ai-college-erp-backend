from django.urls import path
from .views import (
    FacultyListCreateView,
    FacultyDetailView,
    SubjectListCreateView,
    SubjectDetailView
)

urlpatterns = [
    path('faculty/', FacultyListCreateView.as_view()),
    path('faculty/<int:pk>/', FacultyDetailView.as_view()),

    path('subjects/', SubjectListCreateView.as_view()),
    path('subjects/<int:pk>/', SubjectDetailView.as_view()),
]