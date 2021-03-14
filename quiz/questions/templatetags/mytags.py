from django import template
from questions.models import CorrectAnswer
register = template.Library()

@register.simple_tag
def is_right_answer(question , quiz , option):
    print(question , quiz , option )
    answers = CorrectAnswer.objects.filter(question=question)
    for a in answers:
        if a.answer==option:
            return 'bg-success text-light'
    return ''