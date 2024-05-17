from django.contrib.auth.models import User
from django.db import models
from django.db.models import Count

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

class ProfileManager(models.Manager):
    def get_top(self):
        return self.order_by('rating').reverse()[:5]
class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.PROTECT)
    rating = models.IntegerField(default=0)
    avatar = models.ImageField(null=True, blank=True, default='uploads/kot.jpg')
    objects = ProfileManager()
    def __str__(self):
        return str(self.user.username)

class TagManager(models.Manager):
    def get_top(self):
        return self.annotate(cnt = Count("question")).order_by('cnt').reverse()[:5]

class Tag(models.Model):
    title = models.TextField(max_length=30, unique=True)
    objects = TagManager()
    def __str__(self):
        return self.title


class QuestionManager(models.Manager):
    def get_new_question(self):
        return self.order_by('created_at').reverse()
    def get_popular(self):
        return self.order_by('rating').reverse()
    def get_by_tag(self, tag_title):
        return self.filter(tags__title=tag_title)


class Question(models.Model):
    title = models.TextField(max_length=40)
    text = models.TextField()
    author = models.ForeignKey(Profile, on_delete=models.CASCADE)
    tags = models.ManyToManyField(Tag, blank=True)
    rating = models.IntegerField(default=0)
    answers_count = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = QuestionManager()
    def __str__(self):
        return self.title

class AnswerManager(models.Manager):
    def get_answers(self, question):
        return self.filter(question=question).order_by('rating', '-created_at').reverse()


class Answer(models.Model):
    text = models.TextField()
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    author = models.ForeignKey(Profile, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    rating = models.IntegerField(default=0)
    objects = AnswerManager()
    def __str__(self):
        return self.text

class QuestionLike(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    author = models.ForeignKey(Profile, on_delete=models.CASCADE)

class AnswerLike(models.Model):
    answer = models.ForeignKey(Answer, on_delete=models.CASCADE)
    author = models.ForeignKey(Profile, on_delete=models.CASCADE)