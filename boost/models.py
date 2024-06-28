from django.db import models
from django.contrib.auth.models import User

# Create your models here.
# class Branch(models.Model):
#     branch_id = models.IntegerField(primary_key=True)
#     branch_name = models.CharField(max_length=30)

#     def __str__(self):
#         return self.branch_name
    
# class Subject(models.Model):
#     subject_id = models.IntegerField(primary_key=True)
#     subject_name = models.CharField(max_length=30)
#     branch_id = models.ForeignKey(Branch,on_delete=models.CASCADE)

#     def __str__(self):
#         return self.subject_name

# DIFFICULTY_CHOICES = (
#     ('easy', 'Easy'),
#     ('medium', 'Medium'),
#     ('hard', 'Hard'),
# )

# TYPE_CHOICES = (
#     ('mcq', 'MCQ'),
#     ('msq', 'MSQ'),
#     ('nat', 'NAT'),
# )

# class Question(models.Model):
#     question_id = models.IntegerField(primary_key=True)
#     question_text = models.TextField()
#     question_type = models.CharField(max_length=20, choices=TYPE_CHOICES)
#     question_difficulty = models.CharField(max_length=10, choices=DIFFICULTY_CHOICES)
#     subject_id = models.ForeignKey(Subject, on_delete=models.CASCADE)

#     def __str__(self):
#         return self.question_text

# class Answer(models.Model):
#     answer_id = models.IntegerField(primary_key=True)
#     answer_text = models.TextField()
#     is_correct = models.BooleanField()
#     question_id = models.ForeignKey(Question, on_delete=models.CASCADE)

#     def __str__(self):
#         return self.answer_text

# class UserAttempt(models.Model):
#     user_id = models.ForeignKey(User, on_delete=models.CASCADE)
#     question_id = models.ForeignKey(Question, on_delete=models.CASCADE)
#     correctly_answered = models.BooleanField(default=False)

#     def __str__(self):
#         return str(self.user_id) + '_' + str(self.question_id)
    
#     class Meta():
#         unique_together = ('user_id', 'question_id')


# class Solution(models.Model):
#     question_id = models.ForeignKey(Question, on_delete=models.CASCADE)
#     answer = models.TextField()

#     def __str__(self):
#         return self.answer[:11]