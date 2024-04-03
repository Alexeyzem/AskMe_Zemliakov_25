from django.core.paginator import Paginator
from django.http import HttpResponse
from django.shortcuts import render

QUESTIONS = [
    {
        "id": i,
        "title": f'Question {i}',
        "text": f'This is question number {i}',
        "answers": [
            {
                "id":{j},
                "text": f'Answer{j}'
            } for j in range(3)
        ],
        "tags": [
            {
                "id": k,
                "title":f'Tag{k}'
            } for k in range(3)
        ],
    } for i in range(200)
]

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
    page_obj = paginate(QUESTIONS, request, 5)
    return render(request, 'index.html', {"questions": page_obj})


def hot(request):
    questions = QUESTIONS[len(QUESTIONS)-5:]
    return render(request, 'hot.html', {"questions": questions})

def question(request, question_id):
    item = QUESTIONS[question_id]
    return render(request, 'question.html', {"item": item})


def new_question(request):
    return render(request, 'ask.html')


def tags(request, tag_id):
    page_obj = paginate(QUESTIONS, request, 3)
    return render(request, 'tags.html', {"questions": page_obj, "tag":tag_id})


def settings(request):
    return render(request, 'settings.html')


def log_out(request):
    return HttpResponse('logout')


def sign_up(request):
    return render(request, 'signup.html')


def members(request):
    return HttpResponse('members')


def login(request):
    return render(request, 'login.html')