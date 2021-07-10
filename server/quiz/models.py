from django.db import models
from ordered_model.models import OrderedModel
from django.contrib.auth import get_user_model

User = get_user_model()

# Create your models here.
class Quiz(OrderedModel):
    """main quiz model"""

    created_on = models.DateTimeField(auto_now_add=True, db_index=True)
    updated_on = models.DateTimeField(auto_now=True, db_index=True)
    name = models.CharField("Name of Quiz", max_length=200, null=True, blank=True)
    topic = models.CharField(max_length=200, null=True, blank=True)
    time_per_question = models.PositiveIntegerField(
        help_text="time in seconds", default=0
    )
    marks_per_question = models.PositiveIntegerField(default=0)
    live_since = models.DateTimeField(null=True, blank=True, db_index=True)
    available_till = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return self.name or str(self.id)


class TextQuestion(OrderedModel):
    """MCQ Question model"""

    quiz = models.ForeignKey(
        Quiz, on_delete=models.CASCADE, related_name="quiz_text_questions"
    )
    created_on = models.DateTimeField(auto_now_add=True, db_index=True)
    updated_on = models.DateTimeField(auto_now=True, db_index=True)
    text = models.TextField(null=True, blank=True)
    image = models.ImageField(upload_to="quiz/questions", null=True, blank=True)
    answer_text = models.TextField(null=True, blank=True)
    answer_image = models.ImageField(
        upload_to="quiz/questions/answers", null=True, blank=True
    )

    def __str__(self):
        return self.text or self.id


class McqQuestion(OrderedModel):
    """MCQ Question model"""

    quiz = models.ForeignKey(
        Quiz, on_delete=models.CASCADE, related_name="quiz_mcq_questions"
    )
    created_on = models.DateTimeField(auto_now_add=True, db_index=True)
    updated_on = models.DateTimeField(auto_now=True, db_index=True)
    text = models.TextField(null=True, blank=True)
    image = models.ImageField(upload_to="quiz/questions", null=True, blank=True)
    answer_text = models.TextField(null=True, blank=True)
    answer_image = models.ImageField(
        upload_to="quiz/questions/answers", null=True, blank=True
    )

    def __str__(self):
        return self.text or self.id


class Option(OrderedModel):
    """MCQ Question model"""

    question = models.ForeignKey(
        McqQuestion, on_delete=models.CASCADE, related_name="mcq_question_options"
    )
    created_on = models.DateTimeField(auto_now_add=True, db_index=True)
    updated_on = models.DateTimeField(auto_now=True, db_index=True)
    text = models.TextField(null=True, blank=True)
    image = models.ImageField(upload_to="quiz/options", null=True, blank=True)
    is_true = models.BooleanField(default=False)

    def __str__(self):
        return self.text or self.id


class QuizResult(models.Model):
    """model to store quiz result user wise"""

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="user_quizes")
    quiz = models.ForeignKey(
        Quiz,
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="quiz_results",
    )
    created_on = models.DateTimeField(auto_now_add=True, db_index=True)
    updated_on = models.DateTimeField(auto_now=True, db_index=True)
    marks_obtained = models.IntegerField(default=0, db_index=True)

    def __str__(self):
        return self.user or self.id


class UserMcqQuestionResponse(models.Model):
    """model to store user response of MCQ questions"""

    result = models.ForeignKey(
        QuizResult,
        on_delete=models.CASCADE,
        related_name="result_mcq_question_responses",
    )
    question = models.ForeignKey(
        McqQuestion,
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="mcq_question_responses",
    )
    marked_option = models.ForeignKey(
        Option,
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="option_marked_reponses",
    )
    is_correct = models.BooleanField(default=False)

    def __str__(self):
        return self.marked_option or self.id


class UserTextQuestionResponse(models.Model):
    """model to store user response of MCQ questions"""

    result = models.ForeignKey(
        QuizResult,
        on_delete=models.CASCADE,
        related_name="result_text_question_responses",
    )
    question = models.ForeignKey(
        McqQuestion,
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="text_question_responses",
    )
    text = models.TextField(null=True, blank=True)
    is_correct = models.BooleanField(default=False)

    def __str__(self):
        return self.text or self.id
