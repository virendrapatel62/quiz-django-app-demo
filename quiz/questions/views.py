from django.shortcuts import render , HttpResponse , redirect
from .models import Quiz , CorrectAnswer , Question
from django.contrib.auth.forms import AuthenticationForm , UserCreationForm 
from django.contrib.auth import authenticate , login , logout
from django.contrib.auth.decorators import login_required
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
    

    