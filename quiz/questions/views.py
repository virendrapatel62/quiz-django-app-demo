from django.shortcuts import render , HttpResponse
from .models import Quiz , CorrectAnswer , Question
# Create your views here.

def home(request):
    quizes = Quiz.objects.all()
    context = {
        'quizes' : quizes
    }
    return render(request , template_name='quizes/all-quizes.html' , context=context  )


def quizPage(request , quizid):
    quiz = Quiz.objects.get(id=quizid)
    template_name = 'quizes/question-page.html'
    question = None;
    current_question_number = 1

    try:
        if request.method == 'GET':
            question = quiz.question_set.all()[current_question_number-1]
        else:
            print(request.POST)
            current_question_number = int(request.POST.get("next_question_number"))
            questionid = request.POST.get('id')
            userAnswers = request.POST.getlist('answer')
            userAnswers.sort()
            correctAnswersList = []
            correctAnswers = CorrectAnswer.objects.filter(question=Question(id=questionid))
            print("Correct Answers")
            for ans in correctAnswers:
                correctAnswersList.append(ans.answer)
            print("Corrent Answers " , correctAnswersList)
            print("Your Answers " , userAnswers)
            if correctAnswersList==userAnswers:
                print("Got 1 Mark")
            else:
                print("Got 0 Mark")
            question = quiz.question_set.all()[current_question_number-1]
    
        context  = {
            'quiz' : quiz , 
            'question' : question , 
            "next_question_number" : current_question_number+1, 
            "current_question_number" : current_question_number
        }
    
        return render(request=request , template_name = template_name , context=context)

    except IndexError:
        return HttpResponse("No More Questions...")
    

    