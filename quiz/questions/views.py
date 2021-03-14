from django.shortcuts import render , HttpResponse , redirect
from .models import Quiz , CorrectAnswer , Question , UserQuiz , UserAnswer
from django.contrib.auth.forms import AuthenticationForm , UserCreationForm 
from django.contrib.auth import authenticate , login , logout
from django.contrib.auth.decorators import login_required
from datetime import datetime
from django.utils.dateparse import parse_datetime 
# Create your views here.

@login_required(login_url='/accounts/login')
def home(request):
    quizes = Quiz.objects.all()
    context = {
        'quizes' : quizes
    }
    return render(request , template_name='quizes/all-quizes.html' , context=context  )


def loginView(request):
    form = AuthenticationForm()
    if request.method == 'POST':
        form = AuthenticationForm(data = request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(request=request , username=username , password=password)
            print(user)
            if user is not None:
                login(request , user)
                return redirect('home')
        

    # if get Request
    context = {
        'form' : form
    }
    return render(request , template_name='auth/login.html' , context=context )

def register(request):
    form = UserCreationForm()
    
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')

    
    
    context = {
        'form' : form
    }
    return render(request , template_name='auth/register.html' , context=context )

def logoutUser(request):
    logout(request)
    return redirect('login')

@login_required(login_url='/accounts/login')
def quizPage(request , quizid):
    quiz = Quiz.objects.get(id=quizid)
    template_name = 'quizes/question-page.html'
    question = None;
    current_question_number = 1
    user = None
    if request.user.is_authenticated:
        user = request.user

    try:
        if request.method == 'GET':
            userQuiz = UserQuiz(user = user , quiz = quiz)
            userQuiz.save()
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

            userQuiz = UserQuiz.objects.filter(user = user , quiz = quiz)
            userQuiz = userQuiz[len(userQuiz)-1]

            for ans in userAnswers:
                userAnswer = UserAnswer(user_quiz=userQuiz , question=Question(id=questionid) , answer=ans)
                userAnswer.save()

            if correctAnswersList==userAnswers:
                userQuiz.right_answers = userQuiz.right_answers+1 
            else:
                userQuiz.wrong_answers = userQuiz.wrong_answers+1 

            userQuiz.save() 
            question = quiz.question_set.all()[current_question_number-1]
    
        context  = {
            'quiz' : quiz , 
            'question' : question , 
            "next_question_number" : current_question_number+1, 
            "current_question_number" : current_question_number
        }
    
        return render(request=request , template_name = template_name , context=context)

    except IndexError:
        userQuiz = UserQuiz.objects.filter(user = user , quiz = quiz)
        userQuiz = userQuiz[len(userQuiz)-1]
        userQuiz.end_time=datetime.now()
        userQuiz.save()
        print(parse_datetime(userQuiz.end_time.__str__()))
        print(parse_datetime(userQuiz.start_time.__str__()))
        time_taken = parse_datetime(userQuiz.end_time.__str__())-parse_datetime(userQuiz.start_time.__str__())
        return render(request=request , template_name='quizes/quiz-result.html' , context={'result' : userQuiz , 'time_taken' : time_taken})
    

    
@login_required(login_url='/accounts/login')
def allQuizAttempedByUser(request , userQuizId=None):
    if userQuizId is not None:
        user_quiz = UserQuiz.objects.get(id = userQuizId)
        context = {
            'user_quiz' : user_quiz
        }
        return render(request=request ,template_name='quizes/quizes_answers_history.html' , context=context)
    
    # all quizes list
    user = request.user
    userQuizes = UserQuiz.objects.filter(user = user)
    context = {
        'user' : user, 
        'userQuizes' : userQuizes
    }
    return render(request=request , template_name='quizes/quizes_attemped_by_user.html' , context=context)