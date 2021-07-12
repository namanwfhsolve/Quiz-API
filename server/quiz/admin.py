from django import forms
from django.contrib import admin
from django.db import models
from ordered_model.admin import OrderedModelAdmin
from nested_admin.nested import (
    NestedStackedInline,
    NestedTabularInline,
    NestedModelAdmin,
)

from .models import (
    Quiz,
    McqQuestion,
    TextQuestion,
    Option,
    QuizResult,
    UserMcqQuestionResponse,
    UserTextQuestionResponse,
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


class OptionInline(NestedTabularInline):
    formfield_overrides = {
        models.TextField: {
            "widget": forms.Textarea(
                attrs={"rows": 1, "cols": 40, "style": "width: 48em;"}
            )
        }
    }
    model = Option

    def get_extra(self, request, obj=None, **kwargs):
        extra = 4
        if obj:
            return extra - obj.mcq_question_options.count()
        return extra


class McqQuestionInline(NestedStackedInline):
    model = McqQuestion
    formfield_overrides = {
        models.TextField: {
            "widget": forms.Textarea(
                attrs={"rows": 3, "cols": 40, "style": "width: 48em;"}
            )
        }
    }
    extra = 0
    inlines = [OptionInline]


class QuizAdmin(NestedModelAdmin, OrderedModelAdmin):
    inlines = [McqQuestionInline]
    list_display = (
        "name",
        "topic",
        "live_since",
        "available_till",
        "move_up_down_links",
    )


admin.site.register(Quiz, QuizAdmin)
admin.site.register(McqQuestion, McqQuestionAdmin)
admin.site.register(TextQuestion, TextQuestionAdmin)
admin.site.register(Option, OptionAdmin)
admin.site.register(QuizResult)
admin.site.register(UserMcqQuestionResponse)
admin.site.register(UserTextQuestionResponse)
