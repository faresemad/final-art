from django.db import models
from django.contrib.auth import get_user_model
from colleges.models import College
from exams.models import MCQExam, HandDrawingExam, DigitalDrawingExam, PracticeDrawingExam
User = get_user_model()


class Student(models.Model):
    division_option = (
        ("1", "رياضة"),
        ("2", "علوم"),
        ("3", "ادبي")
    )
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='student')
    full_name = models.CharField(max_length=100)
    student_photo = models.ImageField(upload_to='student/%y/%m/%d/', unique=True)
    national_id = models.CharField(max_length=14, unique=True)
    seat_number = models.IntegerField(unique=True)
    total = models.DecimalField(decimal_places=2, max_digits=10)
    division = models.CharField(max_length=100, choices=division_option)
    phone_number = models.CharField(max_length=15, unique=True)
    college = models.ForeignKey(College, on_delete=models.CASCADE, related_name='studentCollege')

    def __str__(self):
        return self.full_name
    
    class Meta:
        verbose_name_plural = "Students"


class McqAnswer(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE,related_name='student_mcq')
    question = models.ForeignKey(MCQExam, on_delete=models.CASCADE,related_name='mcq')
    answer = models.CharField(max_length=100)
    is_correct = models.BooleanField(default=False)
    # score = models.IntegerField(default=0) # increase score if answer is correct
    
    class Meta:
        verbose_name_plural = "Student Answer Mcq"

    def __str__(self):
        return self.answer


class HandDrawingAnswer(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE,related_name='hand_sketch_answer')
    hand_draw = models.ForeignKey(HandDrawingExam, on_delete=models.CASCADE,related_name='hand_sketch')
    answer = models.ImageField(upload_to='student/%y/%m/%d/', unique=True)
    
    class Meta:
        verbose_name_plural = "Student Answer Hand Drawing"

    def __str__(self):
        return self.answer


class DigitalDrawingAnswer(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE,related_name='digital_sketch_answer')
    digital_draw = models.ForeignKey(DigitalDrawingExam, on_delete=models.CASCADE,related_name='digital_sketch')
    answer = models.ImageField(upload_to='student/%y/%m/%d/', unique=True)
    
    class Meta:
        verbose_name_plural = "Student Answer Digital Drawing"

    def __str__(self):
        return self.answer


class PracticeDrawingAnswer(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE,related_name='practice_sketch_answer')
    practice_draw = models.ForeignKey(PracticeDrawingExam, on_delete=models.CASCADE,related_name='practice_sketch')
    answer = models.ImageField(upload_to='student/%y/%m/%d/', unique=True)
    
    class Meta:
        verbose_name_plural = "Student Answer Practice Drawing"

    def __str__(self):
        return self.answer


class StudentResults(models.Model):
    user = models.OneToOneField(Student, on_delete=models.CASCADE, related_name='student_result')
    mcq_result = models.IntegerField(null=True, blank=True, default=0)
    digital_art_result = models.IntegerField(null=True, blank=True, default=0)
    hand_drawing_result = models.IntegerField(null=True, blank=True, default=0)
    trial_result = models.IntegerField(null=True, blank=True, default=0)
    up_to_level = models.BooleanField(default=False)
    
    class Meta:
        verbose_name_plural = "Student Results"