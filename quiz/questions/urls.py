
from django.contrib import admin
from django.urls import path , include
from questions.views import home , quizPage , loginView , register , logoutUser , allQuizAttempedByUser

urlpatterns = [
    path('' , home , name='home'), 
    path('accounts/login' , loginView , name='login'), 
    path('accounts/register' , register), 
    path('accounts/logout' , logoutUser), 
    path('quiz/<int:quizid>' , quizPage), 
    path('profile/history/quizes' , allQuizAttempedByUser), 
    path('profile/history/quizes/<int:userQuizId>' , allQuizAttempedByUser), 
]
