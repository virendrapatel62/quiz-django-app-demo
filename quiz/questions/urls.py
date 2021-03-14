
from django.contrib import admin
from django.urls import path , include
from questions.views import home , quizPage , loginView , register , logoutUser

urlpatterns = [
    path('' , home , name='home'), 
    path('accounts/login' , loginView , name='login'), 
    path('accounts/register' , register), 
    path('accounts/logout' , logoutUser), 
    path('quiz/<int:quizid>' , quizPage), 
]
