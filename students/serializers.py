import os
import uuid

from django.conf import settings
from django.contrib.auth import get_user_model
from django.db.models import Sum
from rest_framework import serializers

from exams.models import (
    DigitalDrawingExam,
    HandDrawingExam,
    MCQExam,
    PracticeDrawingExam,
)

from .models import (
    DigitalDrawingAnswer,
    HandDrawingAnswer,
    McqAnswer,
    PracticeDrawingAnswer,
    Student,
    StudentResults,
)

User = get_user_model()


class StudentSerializer(serializers.ModelSerializer):
    national_id = serializers.CharField(required=False)

    class Meta:
        model = Student
        fields = "__all__"
        read_only_fields = ["up_to_level", "user"]

    def get_user(self, obj):
        return obj.user.email

    def get_college(self, obj):
        return obj.college.name

    def __init__(self, instance=None, **kwargs):
        super().__init__(instance, **kwargs)
        self.fields["user"].queryset = User.objects.filter(
            id=self.context["request"].user.id
        )

    def create(self, validated_data):
        user = self.context["request"].user
        try:
            student = user.student
        except Student.DoesNotExist:
            student = None
        if student is not None:
            # update existing student object
            student.full_name = validated_data.get("full_name", student.full_name)
            student.student_photo = validated_data.get(
                "student_photo", student.student_photo
            )
            # update other fields as needed
            student.save()
            return student
        else:
            # create new student object
            validated_data["user"] = user
            national_id = validated_data.get("national_id")
            student_photo = validated_data.get("student_photo")
            if national_id and student_photo:
                file_ext = student_photo.name.split(".")[-1]
                filename = f"{national_id}.{file_ext}"
                # update path if filename already exists
                if os.path.exists(
                    os.path.join(settings.MEDIA_ROOT, "students", filename)
                ):
                    filename = f"{national_id}_{uuid.uuid4().hex}.{file_ext}"
                validated_data["student_photo"].name = filename
            return super().create(validated_data)

    def update(self, instance, validated_data):
        national_id = validated_data.get("national_id")
        student_photo = validated_data.get("student_photo")
        if national_id and student_photo:
            file_ext = student_photo.name.split(".")[-1]
            filename = f"{national_id}.{file_ext}"
            # update path if filename already exists
            if os.path.exists(os.path.join(settings.MEDIA_ROOT, "students", filename)):
                filename = f"{national_id}_{uuid.uuid4().hex}.{file_ext}"
            validated_data["student_photo"].name = filename
        return super().update(instance, validated_data)

    def update_up_to_level(self, student):
        score_mcq = student.student_mcq.aggregate(Sum("score"))["score__sum"]
        score_hand_sketch = student.hand_sketch_answer.aggregate(Sum("score"))[
            "score__sum"
        ]
        score_digital_sketch = student.digital_sketch_answer.aggregate(Sum("score"))[
            "score__sum"
        ]
        score_practice_sketch = student.practice_sketch_answer.aggregate(Sum("score"))[
            "score__sum"
        ]
        score_sum = sum(
            filter(
                None,
                [
                    score_mcq,
                    score_hand_sketch,
                    score_digital_sketch,
                    score_practice_sketch,
                ],
            )
        )

        score_sum = score_sum or 0
        if score_sum >= 150 and score_sum < 400:
            student.up_to_level = True
        else:
            student.up_to_level = False
        student.save()

    def to_representation(self, instance):
        self.update_up_to_level(instance)
        representation = super().to_representation(instance)
        representation["student_photo_name"] = instance.student_photo.name.split("/")[
            -1
        ]
        return representation


class McqAnswerSerializer(serializers.ModelSerializer):
    question = serializers.PrimaryKeyRelatedField(queryset=MCQExam.objects.none())
    is_correct = serializers.SerializerMethodField()

    class Meta:
        model = McqAnswer
        fields = ["question", "answer", "is_correct"]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        user = self.context["request"].user
        if hasattr(user, "student"):
            self.fields["question"].queryset = MCQExam.objects.filter(
                college=user.student.college
            )
        else:
            self.fields["question"].queryset = MCQExam.objects.none()

    def get_is_correct(self, obj):
        return obj.is_correct

    def create(self, validated_data):
        validated_data["student"] = self.context["request"].user.student
        try:
            answer = McqAnswer.objects.get(
                student=validated_data["student"], question=validated_data["question"]
            )
            prev_answer = answer.answer
            answer.answer = validated_data["answer"]
            if answer.answer == answer.question.answer:
                if prev_answer != answer.answer:
                    answer.score += 1
            else:
                if prev_answer == answer.question.answer:
                    answer.score -= 1
        except McqAnswer.DoesNotExist:
            answer = McqAnswer.objects.create(**validated_data)
            if answer.answer == answer.question.answer:
                answer.score += 1
        answer.is_correct = answer.answer == answer.question.answer
        answer.save()
        return answer


class HandDrawingSerializer(serializers.ModelSerializer):
    hand_draw = serializers.PrimaryKeyRelatedField(
        queryset=HandDrawingExam.objects.none()
    )

    class Meta:
        model = HandDrawingAnswer
        fields = ["hand_draw", "answer"]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        user = self.context["request"].user
        if hasattr(user, "student"):
            self.fields["hand_draw"].queryset = HandDrawingExam.objects.filter(
                college=user.student.college
            )
        else:
            self.fields["hand_draw"].queryset = HandDrawingExam.objects.none()

    def create(self, validated_data):
        validated_data["student"] = self.context["request"].user.student
        try:
            answer = HandDrawingAnswer.objects.get(
                student=validated_data["student"], hand_draw=validated_data["hand_draw"]
            )
            answer.answer = validated_data["answer"]
            answer.save()
            return answer

        except HandDrawingAnswer.DoesNotExist:
            return HandDrawingAnswer.objects.create(**validated_data)


class DigitalSerializer(serializers.ModelSerializer):
    digital_draw = serializers.PrimaryKeyRelatedField(
        queryset=DigitalDrawingExam.objects.none()
    )

    class Meta:
        model = DigitalDrawingAnswer
        fields = ["digital_draw", "answer"]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        user = self.context["request"].user
        if hasattr(user, "student"):
            self.fields["digital_draw"].queryset = DigitalDrawingExam.objects.filter(
                college=user.student.college
            )
        else:
            self.fields["digital_draw"].queryset = DigitalDrawingExam.objects.none()

    def create(self, validated_data):
        validated_data["student"] = self.context["request"].user.student
        try:
            answer = DigitalDrawingAnswer.objects.get(
                student=validated_data["student"],
                digital_draw=validated_data["digital_draw"],
            )
            answer.answer = validated_data["answer"]
            answer.save()
            return answer

        except DigitalDrawingAnswer.DoesNotExist:
            return DigitalDrawingAnswer.objects.create(**validated_data)


class PracticeSerializer(serializers.ModelSerializer):
    practice_draw = serializers.PrimaryKeyRelatedField(
        queryset=PracticeDrawingExam.objects.none()
    )

    class Meta:
        model = PracticeDrawingAnswer
        fields = ["practice_draw", "answer"]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        user = self.context["request"].user
        if hasattr(user, "student"):
            self.fields["practice_draw"].queryset = PracticeDrawingExam.objects.filter(
                college=user.student.college
            )
        else:
            self.fields["practice_draw"].queryset = PracticeDrawingExam.objects.none()

    def create(self, validated_data):
        validated_data["student"] = self.context["request"].user.student
        try:
            answer = PracticeDrawingAnswer.objects.get(
                student=validated_data["student"],
                practice_draw=validated_data["practice_draw"],
            )
            answer.answer = validated_data["answer"]
            answer.save()
            return answer

        except PracticeDrawingAnswer.DoesNotExist:
            return PracticeDrawingAnswer.objects.create(**validated_data)


class UserResultSerializer(serializers.ModelSerializer):
    class Meta:
        model = Student
        fields = ["id", "full_name"]


class StudentResultsSerializer(serializers.ModelSerializer):
    user = UserResultSerializer(read_only=True)

    class Meta:
        model = StudentResults
        fields = [
            "user",
            "mcq_result",
            "digital_art_result",
            "hand_drawing_result",
            "trial_result",
            "up_to_level",
        ]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        user = self.context["request"].user
        if hasattr(user, "student"):
            self.fields["user"].queryset = Student.objects.filter(
                college=user.student.college
            )
        else:
            self.fields["user"].queryset = Student.objects.none()

    def create(self, validated_data):
        return StudentResults.objects.create(**validated_data)
