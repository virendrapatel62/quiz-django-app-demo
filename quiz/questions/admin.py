from django.contrib import admin 
from questions.models import Question , Quiz , CorrectAnswer
# Register your models here.
class CorrectAnswerAdminModel(admin.TabularInline):
    model = CorrectAnswer

class QuestionAdminModel(admin.ModelAdmin):
    model=Question
    inlines=[CorrectAnswerAdminModel]

admin.site.register(Question , QuestionAdminModel)
admin.site.register(Quiz )