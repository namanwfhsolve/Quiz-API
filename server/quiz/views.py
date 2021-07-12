from rest_framework import generics
from rest_framework.permissions import IsAdminUser, IsAuthenticated
from url_filter.integrations.drf import DjangoFilterBackend
from django.utils import timezone as tz

from .serializer import QuizListSerializer, QuizDetailSerializer
from .models import Quiz


class QuizView(generics.ListAPIView):
    serializer_class = QuizListSerializer
    queryset = Quiz.objects.order_by("-live_since", "order")
    filter_backends = [DjangoFilterBackend]
    filter_fields = ["live_since", "available_till"]


class QuizDetailView(generics.RetrieveUpdateAPIView):
    serializer_class = QuizDetailSerializer
    queryset = Quiz.objects.prefetch_related(
        "quiz_mcq_questions__mcq_question_options", "quiz_text_questions"
    )


class QuizCreateView(generics.CreateAPIView):
    serializer_class = QuizDetailSerializer
    queryset = Quiz.objects.prefetch_related(
        "quiz_mcq_questions__mcq_question_options", "quiz_text_questions"
    )
    permission_classes = [IsAdminUser]
