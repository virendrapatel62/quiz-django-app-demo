from django.contrib import admin 
from questions.models import Question , Quiz , CorrectAnswer  , UserQuiz , UserAnswer
# Register your models here.
class CorrectAnswerAdminModel(admin.TabularInline):
    model = CorrectAnswer

class QuestionAdminModel(admin.ModelAdmin):
    model=Question
    inlines=[CorrectAnswerAdminModel]

admin.site.register(Question , QuestionAdminModel)
admin.site.register(Quiz )
admin.site.register(UserQuiz )
admin.site.register(UserAnswer)