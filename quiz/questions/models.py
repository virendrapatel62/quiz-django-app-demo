from django.db import models

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
    choices = [('A' , 'a') , ('B' , 'b') , ('C' , 'c') , ("D" , 'd')]
    question = models.ForeignKey(Question , on_delete=models.CASCADE)
    answer = models.CharField(max_length=100 , choices = choices)
   