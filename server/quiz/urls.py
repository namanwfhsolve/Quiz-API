from django.urls import path

from .views import QuizView, QuizDetailView, QuizCreateView

urlpatterns = [
    path("quizes/", QuizView.as_view(), name="quiz_list_create"),
    path("quiz/create/", QuizCreateView.as_view(), name="quiz_create"),
    path("quiz/<int:pk>/", QuizDetailView.as_view(), name="quiz_retrive_update"),
]
