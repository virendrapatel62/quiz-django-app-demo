
from django.contrib import admin
from django.urls import path , include
from questions.views import home , quizPage

urlpatterns = [
    path('' , home), 
    path('quiz/<int:quizid>' , quizPage), 
]
