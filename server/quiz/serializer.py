from rest_framework import serializers

from django.utils import timezone as tz

from .models import Quiz, McqQuestion, TextQuestion, Option


class QuizSerializer(serializers.ModelSerializer):
    def validate_live_since(self, time):
        # if live since is less than now
        # raise error
        if time < tz.localtime():
            raise serializers.ValidationError(
                f"live_since cannot be less than {tz.localtime()}"
            )
        return time

    def validate_available_till(self, time):
        # if available is less than now
        # raise error
        if time < tz.localtime():
            raise serializers.ValidationError(
                f"available_till cannot be less than {tz.localtime()}"
            )
        return time

    def validate(self, attrs):
        if attrs["live_since"] > attrs["available_till"]:
            raise serializers.ValidationError(
                {"time_error": "live_since cannot ber greater that available_till"}
            )

        return super().validate(attrs)

    class Meta:
        model = Quiz
        fields = "__all__"


class McqQuestionSerializer(serializers.ModelSerializer):
    class Meta:
        model = McqQuestion
        fields = "__all__"


class TextQuestionSerializer(serializers.ModelSerializer):
    def validate(self, attrs):
        if not (attrs.get("text") or attrs.get("image")):
            raise serializers.ValidationError(
                {"text_image": "Either text or image is required"}
            )

        if not (attrs.get("answer_text") or attrs.get("answer_image")):
            raise serializers.ValidationError(
                {"answer_text_image": "Either text or image is required"}
            )

        return attrs

    class Meta:
        model = TextQuestion
        fields = "__all__"
        extra_kwargs = {"quiz": {"required": False}}


class OptionSerializer(serializers.ModelSerializer):
    def validate(self, attrs):
        if not (attrs.get("text") or attrs.get("image")):
            raise serializers.ValidationError(
                {"text_image": "Either text or image is required"}
            )

        return attrs

    class Meta:
        model = Option
        fields = "__all__"
        extra_kwargs = {"question": {"required": False}}


class QuizListSerializer(QuizSerializer):
    class Meta:
        model = Quiz
        fields = "__all__"


class McqQuestionDetailSerializer(McqQuestionSerializer):
    options = OptionSerializer(source="mcq_question_options", many=True)

    def validate(self, attrs):
        if not (attrs.get("text") or attrs.get("image")):
            raise serializers.ValidationError(
                {"text_image": "Either text or image is required"}
            )

        if not (attrs.get("answer_text") or attrs.get("answer_image")):
            raise serializers.ValidationError(
                {"answer_text_image": "Either text or image is required"}
            )

        return attrs

    class Meta(McqQuestionSerializer.Meta):
        fields = ["id", "text", "image", "options", "answer_text", "answer_image"]

    def create(self, validated_data):
        options = validated_data.pop("mcq_question_options", [])
        # print(options, validated_data)

        question = super().create(validated_data)

        # saving the options
        for option in options:
            print(option, question, question.id)
            # Option.objects.create(**option, question=question)

        return question


class QuizDetailSerializer(QuizSerializer):
    mcq_questions = McqQuestionDetailSerializer(source="quiz_mcq_questions", many=True)
    text_questions = TextQuestionSerializer(source="quiz_text_questions", many=True)

    class Meta(QuizListSerializer.Meta):
        fields = [
            "id",
            "name",
            "topic",
            "time_per_question",
            "marks_per_question",
            "live_since",
            "available_till",
            "mcq_questions",
            "text_questions",
        ]

        extra_kwargs = {
            "name": {"required": True},
            "topic": {"required": True},
            "time_per_question": {"required": True},
            "marks_per_question": {"required": True},
            "live_since": {"required": True},
            "available_till": {"required": True},
        }

    def create(self, validated_data):
        # pop out the related object mcq and text qestions
        mcq_questions = validated_data.pop("quiz_mcq_questions", [])
        text_questions = validated_data.pop("quiz_text_questions", [])

        # save the quiz first to get id
        quiz = super().create(validated_data)

        # saving the mcq questions
        for question in mcq_questions:
            options = question.pop("mcq_question_options", [])
            ques = McqQuestion.objects.create(**question, quiz=quiz)
            Option.objects.bulk_create(
                [Option(**option, question=ques) for option in options]
            )

        # saving the mcq questions
        for question in text_questions:
            TextQuestion.objects.create(**question, quiz=quiz)

        return quiz
