from django.contrib import auth
from django.contrib.auth import authenticate
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.forms import forms
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from django.views.decorators.csrf import csrf_protect
from django.views.decorators.http import require_http_methods
from app import models
from app.forms import LoginForm, RegisterForm, AskForm, AnswerForm, SettingsForm
from django.core.cache import cache
import json

def cache_data():
    best_tags = cache.get('best_tags')
    best_members = cache.get('best_members')
    return best_tags, best_members
def paginate(obj_list, request, per_page):
    paginator = Paginator(obj_list, per_page)
    page_num = request.GET.get('page', 1)
    try:
        p = int(page_num)
        if p < 1:
            page_num = 1
    except ValueError:
        page_num = 1
    page_obj = paginator.get_page(page_num)
    num = int(page_num)
    if page_obj.has_next() and num + 3 <= paginator.num_pages:
        a = range(int(page_num)+1, int(page_num)+4)
    elif not(page_obj.has_next()):
        a = range(1, 2)
    else:
        a = range(int(page_num)+1, paginator.num_pages+1)
    page_obj.page_range = a
    return page_obj

def index(request):
    questions = models.Question.objects.get_new_question()
    page_obj = paginate(questions, request, 5)
    best_tags, best_members = cache_data()
    return render(request, 'index.html', {"questions": page_obj, "best_members": best_members, "best_tags": best_tags})


def hot(request):
    questions = models.Question.objects.get_popular()
    page_obj = paginate(questions, request, 5)
    best_tags, best_members = cache_data()
    return render(request, 'hot.html', {"questions": page_obj, "best_members": best_members, "best_tags": best_tags})

@require_http_methods(['GET', 'POST'])
@csrf_protect
def question(request, question_id):
    item = models.Question.objects.get(id=question_id)
    answers = models.Answer.objects.get_answers(item.id)
    answers = paginate(answers, request, 5)
    best_tags, best_members = cache_data()
    if request.method == "POST":
        answer_form = AnswerForm(request.POST)
        if answer_form.is_valid():
            answer = answer_form.save(author=models.Profile.objects.get(user__username=request.user.username), question=models.Question.objects.get(id=item.id))
            if answer:
                answers = models.Answer.objects.get_answers(item.id)
                answers = paginate(answers, request, 5)
                item.answers_count += 1
                return render(request, 'question.html', {"item": item, "answers":answers, "best_members": best_members, "best_tags": best_tags, "form": answer_form})
    if request.method == 'GET':
        answer_form = AnswerForm()
    return render(request, 'question.html', {"item": item, "answers":answers, "best_members": best_members, "best_tags": best_tags ,"form": answer_form})

def tags(request, tag_title):
    questions = models.Question.objects.get_by_tag(tag_title)
    page_obj = paginate(questions, request, 3)
    best_tags, best_members = cache_data()
    return render(request, 'tags.html', {"questions": page_obj, "tag":tag_title, "best_members": best_members,"best_tags": best_tags })

@login_required(redirect_field_name='login', login_url='/login')
@require_http_methods(['GET', 'POST'])
@csrf_protect
def settings(request):
    best_tags, best_members = cache_data()
    if request.method == "POST":
        user_from_db = models.User.objects.get(username=request.user.username)
        setting_form = SettingsForm(request.POST, request.FILES, user_from_db)
        if setting_form.is_valid():
            user = setting_form.save(user=user_from_db)
            if user:
                auth.login(request, user)
                return redirect(reverse("settings"))
            else:
                setting_form.add_error("can not update user's data")
    if request.method == "GET":
        setting_form = SettingsForm()
    return render(request, 'settings.html', {"best_members": best_members, "best_tags":best_tags, "form": setting_form})

@login_required(redirect_field_name='login', login_url='/login')
@require_http_methods(['GET', 'POST'])
@csrf_protect
def new_question(request):
    best_tags, best_members = cache_data()
    if request.method == 'GET':
        ask_form = AskForm()
    if request.method == 'POST':
        ask_form = AskForm(request.POST)
        if ask_form.is_valid():
            ques = ask_form.save(author=models.Profile.objects.get(user__username=request.user.username))
            if ques:
                return redirect(reverse("question" , args=[ques.id]))
            else:
                ask_form.add_error(field=None, error="Question was not saved.")
    return render(request, 'ask.html', {"best_members": best_members, "best_tags":best_tags, "form":ask_form})

@require_http_methods(['GET', 'POST'])
@csrf_protect
def sign_up(request):
    if request.method == 'GET':
        signup_form = RegisterForm()
    if request.method == 'POST':
        signup_form = RegisterForm(request.POST, request.FILES)
        if signup_form.is_valid():
            user = signup_form.save()
            if user:
                auth.login(request, user)
                return redirect(reverse('index'))
            else:
                signup_form.add_error(field=None, error="User saving error")
    best_tags, best_members = cache_data()
    return render(request, 'signup.html', {"best_members": best_members, "form":signup_form, "best_tags":best_tags})

@require_http_methods(['GET', 'POST'])
@csrf_protect
def login(request):
    if request.method == 'GET':
        login_form = LoginForm()
        errors = ''
    if request.method == 'POST':
        login_form = LoginForm(data=request.POST)
        if login_form.is_valid():
            user = authenticate(request, **login_form.cleaned_data)
            if user:
                auth.login(request, user)
                return redirect(reverse('index'))
            else:
                errors = 'Wrong username or password'
    best_tags, best_members = cache_data()
    return render(request, 'login.html',{"best_members": best_members, "form": login_form, "errors": errors, "best_tags": best_tags})

@login_required(redirect_field_name='login', login_url='/login')
def log_out(request):
    auth.logout(request)
    return redirect(reverse('index'))
def members(request):
    return HttpResponse('members')

@require_http_methods(['POST'])
@login_required(redirect_field_name='login', login_url='/login')
@csrf_protect
def question_like_async(request, item_id):
    question = get_object_or_404(models.Question, pk=item_id)
    question_like, _ = models.QuestionLike.objects.get_or_create(question=question, author=request.user.profile)
    body = json.loads(request.body)
    updatingInfo = 0
    if body["action"] == "like":
        updatingInfo = 1
    elif body["action"] == "dislike":
        updatingInfo = -1
    if question_like.num == 0:
        question_like.num = updatingInfo
        question_like.save()
        question.rating += updatingInfo
        request.user.profile.rating += updatingInfo
        request.user.profile.save()
        question.save()
    elif question_like.num == updatingInfo:
        question_like.delete()
        question.rating-= updatingInfo
        request.user.profile.rating -= updatingInfo
        request.user.profile.save()
        question.save()
    elif question_like.num == -updatingInfo:
        question_like.num = updatingInfo
        question_like.save()
        request.user.profile.rating += 2*updatingInfo
        request.user.profile.save()
        question.rating += 2*updatingInfo
        question.save()
    body["likes_count"] = question.rating
    return JsonResponse(body)

@require_http_methods(['POST'])
@login_required(redirect_field_name='login', login_url='/login')
@csrf_protect
def answer_like_async(request, item_id):
    answer = get_object_or_404(models.Answer, pk=item_id)
    answer_like, _ = models.AnswerLike.objects.get_or_create(answer=answer, author=request.user.profile)
    body = json.loads(request.body)
    updatingInfo = 0
    if body["action"] == "like":
        updatingInfo = 1
    elif body["action"] == "dislike":
        updatingInfo = -1
    if answer_like.num == 0:
        answer_like.num = updatingInfo
        answer_like.save()
        request.user.profile.rating += updatingInfo
        request.user.profile.save()
        answer.rating += updatingInfo
        answer.save()
    elif answer_like.num == updatingInfo:
        answer_like.delete()
        answer.rating-= updatingInfo
        request.user.profile.rating -= updatingInfo
        request.user.profile.save()
        answer.save()
    elif answer_like.num == -updatingInfo:
        answer_like.num = updatingInfo
        answer_like.save()
        request.user.profile.rating += 2 * updatingInfo
        request.user.profile.save()
        answer.rating += 2*updatingInfo
        answer.save()
    body["likes_count"] = answer.rating
    return JsonResponse(body)

@require_http_methods(['POST'])
@login_required(redirect_field_name='login', login_url='/login')
@csrf_protect
def answer_correct_async(request, item_id):
    answer = get_object_or_404(models.Answer, pk=item_id)
    if answer.correct:
        answer.correct = False
    else:
        answer.correct = True
    answer.save()
    return JsonResponse({'status':'ok'})