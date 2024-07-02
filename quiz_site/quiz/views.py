from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import UserCreationForm
from .models import Topic, Question, QuizAttempt
from .utils import scrape_wikipedia, generate_qa_pairs
import random

def home(request):
    if request.user.is_authenticated:
        attempts = QuizAttempt.objects.filter(user=request.user)
        scores = {topic.name: sum(attempt.is_correct for attempt in attempts if attempt.question.topic.name == topic.name) for topic in Topic.objects.all()}
    else:
        scores = {}
    return render(request, 'quiz/home.html', {'scores': scores})

def about(request):
    return render(request, 'quiz/about.html')

def game(request):
    topics = Topic.objects.all()
    return render(request, 'quiz/game.html', {'topics': topics})

def quiz(request, topic):
    topic_obj = Topic.objects.get(name=topic)
    questions = list(Question.objects.filter(topic=topic_obj))
    if not questions:
        # Scrape Wikipedia and generate questions
        content = scrape_wikipedia(topic)
        qa_pairs = generate_qa_pairs(content)
        for qa in qa_pairs:
            question = Question(topic=topic_obj, **qa)
            question.save()
        questions = list(Question.objects.filter(topic=topic_obj))
    
    question = random.choice(questions)
    options = [question.correct_answer, question.option_1, question.option_2, question.option_3]
    random.shuffle(options)

    if request.method == 'POST':
        selected_option = request.POST.get('option')
        is_correct = selected_option == question.correct_answer
        QuizAttempt.objects.create(user=request.user, question=question, selected_option=selected_option, is_correct=is_correct)
        return redirect('home')
    
    return render(request, 'quiz/quiz.html', {'question': question, 'options': options})

def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('home')
    return render(request, 'quiz/login.html')

def logout_view(request):
    logout(request)
    return redirect('home')

def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')
    else:
        form = UserCreationForm()
    return render(request, 'quiz/register.html', {'form': form})
