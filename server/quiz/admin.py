from django.contrib import admin
from ordered_model.admin import OrderedModelAdmin

from .models import (
    Quiz,
    McqQuestion,
    TextQuestion,
    Option,
    QuizResult,
    UserMcqQuestionResponse,
    UserTextQuestionResponse,
)


class QuizAdmin(OrderedModelAdmin):
    list_display = (
        "name",
        "topic",
        "live_since",
        "available_till",
        "move_up_down_links",
    )


class McqQuestionAdmin(OrderedModelAdmin):
    list_display = (
        "quiz",
        "text",
        "move_up_down_links",
    )


class TextQuestionAdmin(OrderedModelAdmin):
    list_display = (
        "quiz",
        "text",
        "move_up_down_links",
    )


class OptionAdmin(OrderedModelAdmin):
    list_display = (
        "question",
        "text",
        "move_up_down_links",
    )


admin.site.register(Quiz, QuizAdmin)
admin.site.register(McqQuestion, McqQuestionAdmin)
admin.site.register(TextQuestion, TextQuestionAdmin)
admin.site.register(Option, OptionAdmin)
admin.site.register(QuizResult)
admin.site.register(UserMcqQuestionResponse)
admin.site.register(UserTextQuestionResponse)
