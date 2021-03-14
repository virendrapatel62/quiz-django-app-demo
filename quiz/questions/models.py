from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Quiz(models.Model):
    title = models.CharField(max_length=30)

    def __str__(self):
        return self.title


class Question(models.Model):
    quiz=models.ForeignKey(Quiz , on_delete=models.CASCADE)
    question = models.CharField(max_length=300)
    a = models.CharField(max_length=100)
    b = models.CharField(max_length=100)
    c = models.CharField(max_length=100)
    d = models.CharField(max_length=100)
    def __str__(self):
        return self.question




class CorrectAnswer(models.Model):
    choices = [('A' , 'A') , ('B' , 'B') , ('C' , 'C') , ("D" , 'D')]
    question = models.ForeignKey(Question , on_delete=models.CASCADE)
    answer = models.CharField(max_length=100 , choices = choices)

class UserQuiz(models.Model):
    quiz=models.ForeignKey(Quiz , on_delete=models.CASCADE)
    user=models.ForeignKey(User , on_delete=models.CASCADE)
    time=models.DateTimeField(auto_now_add=True)
    right_answers = models.IntegerField(default=0)
    wrong_answers = models.IntegerField(default=0)

class UserAnswer(models.Model):
    choices = [('A' , 'A') , ('B' , 'B') , ('C' , 'C') , ("D" , 'D')]
    user_quiz = models.ForeignKey(UserQuiz , on_delete=models.CASCADE)
    question = models.ForeignKey(Question , on_delete=models.CASCADE)
    answer = models.CharField(max_length=100 , choices = choices)



   