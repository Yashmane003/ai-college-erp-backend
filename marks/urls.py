from django.urls import path
from .views import MarksListCreateView, MarksDetailView

urlpatterns = [
    path('marks/', MarksListCreateView.as_view()),
    path('marks/<int:pk>/', MarksDetailView.as_view()),
]