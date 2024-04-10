from django.core.paginator import Paginator
from django.http import HttpResponse
from django.shortcuts import render
from app import models

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
    obj = models.Question.objects.get_tag(questions)
    obj = models.Answer.objects.get_all_answers(obj)
    page_obj = paginate(obj, request, 5)
    best_members = models.Profile.objects.get_top()
    print(obj[0]['created_at'])
    print(obj[1]['created_at'])
    return render(request, 'index.html', {"questions": page_obj, "best_members": best_members})


def hot(request):
    questions = models.Question.objects.get_popular()
    obj = models.Question.objects.get_tag(questions)
    obj = models.Answer.objects.get_all_answers(obj)
    best_members = models.Profile.objects.get_top()
    return render(request, 'hot.html', {"questions": obj, "best_members": best_members})

def question(request, question_id):
    item = models.Question.objects.get_one(question_id)
    answers = models.Answer.objects.get_answers(item['id'])
    item['answers'] = answers
    best_members = models.Profile.objects.get_top()
    return render(request, 'question.html', {"item": item, "best_members": best_members})


def new_question(request):
    best_members = models.Profile.objects.get_top()
    return render(request, 'ask.html', {"best_members": best_members})


def tags(request, tag_title):
    questions = models.Question.objects.get_by_tag(tag_title)
    obj = models.Question.objects.get_tag(questions)
    page_obj = paginate(obj, request, 3)
    best_members = models.Profile.objects.get_top()
    return render(request, 'tags.html', {"questions": page_obj, "tag":tag_title, "best_members": best_members})


def settings(request):
    best_members = models.Profile.objects.get_top()
    return render(request, 'settings.html', {"best_members": best_members})


def log_out(request):
    return HttpResponse('logout')


def sign_up(request):
    best_members = models.Profile.objects.get_top()
    return render(request, 'signup.html', {"best_members": best_members})


def members(request):
    return HttpResponse('members')


def login(request):
    best_members = models.Profile.objects.get_top()
    return render(request, 'login.html',{"best_members": best_members})