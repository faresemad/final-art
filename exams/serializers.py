from rest_framework import serializers
from .models import MCQExam, DigitalDrawingExam, HandDrawingExam, PracticeDrawingExam
from colleges.models import College

class McqExamSerializer(serializers.ModelSerializer):
    class Meta:
        model = MCQExam
        fields = '__all__'

class DigitalDrawingExamSerializer(serializers.ModelSerializer):
    class Meta:
        model = DigitalDrawingExam
        fields = '__all__'

class HandDrawingExamSerializer(serializers.ModelSerializer):
    class Meta:
        model = HandDrawingExam
        fields = '__all__'

class PracticeDrawingExamSerializer(serializers.ModelSerializer):
    class Meta:
        model = PracticeDrawingExam
        fields = '__all__'

class CollegeSerializer(serializers.ModelSerializer):
    class Meta:
        model = College
        fields = ['id', 'name']