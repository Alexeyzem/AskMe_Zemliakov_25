from django.contrib.auth.models import User
from django.db import models

# Create your models here.


# user field:
# username
# first_name
# last_name
# email
# password
# groups
# user_permissions
# is_staff разрешает доступ к админке
# is_active
# is_superuser  считает пользователя имеющим все разрешения
# last_login - date when user last login
# date_joined - date when the acc created
class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.PROTECT)
    rating = models.IntegerField(default=0)
    avatar = models.ImageField(null=True, blank=True)
    def __str__(self):
        return str(self.user.username)


class Tag(models.Model):
    title = models.TextField(max_length=30, unique=True)
    def __str__(self):
        return self.title


class QuestionManager(models.Manager):
    def get_new_question(self):
        return self.order_by('created_at')
    def get_popular(self):
        return self.order_by('rating')
    def get_by_tag(self, tag_title):
        return self.filter(tags__title=tag_title)
    def add_tag(self, questions):
        question_list = questions.values()
        for i in range(0, len(question_list)):
            tags = Tag.objects.filter(question=question_list[i]['id'])
            question_list[i]["tags"] = tags
        return questions

class Question(models.Model):
    title = models.TextField(max_length=40)
    text = models.TextField()
    author = models.ForeignKey(Profile, on_delete=models.CASCADE)
    tags = models.ManyToManyField(Tag, blank=True)
    rating = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = QuestionManager()
    def __str__(self):
        return self.title

class Answer(models.Model):
    text = models.TextField()
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    author = models.ForeignKey(Profile, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    rating = models.IntegerField(default=0)
    def __str__(self):
        return self.text

class QuestionLike(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    author = models.ForeignKey(Profile, on_delete=models.CASCADE)

class AnswerLike(models.Model):
    answer = models.ForeignKey(Answer, on_delete=models.CASCADE)
    author = models.ForeignKey(Profile, on_delete=models.CASCADE)