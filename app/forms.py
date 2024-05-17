import time
from datetime import datetime

from django import forms
from django.contrib.auth.models import User

from app import models
from app.models import Question, Answer


class LoginForm(forms.Form):
    username = forms.CharField(label='Username',max_length=50, widget=forms.TextInput(attrs={'placeholder': 'Username'}))
    password = forms.CharField(label='Password', widget=forms.PasswordInput(attrs={'placeholder': 'Password'}))



class RegisterForm(forms.ModelForm):
    password = forms.CharField(label='Password', widget=forms.PasswordInput(attrs={'placeholder': 'Password'}))
    repeat_password = forms.CharField(label='Password', widget=forms.PasswordInput(attrs={'placeholder': 'Repeat Password'}))
    avatar = forms.ImageField(label='Avatar', required=False)
    class Meta:
        model = User
        fields = ['username', 'email', 'password']
    def clean(self):
        super().clean()
        if self.cleaned_data['password'] != self.cleaned_data['repeat_password']:
            raise forms.ValidationError('Passwords do not match')
    def save(self, commit=True):
        user = super(RegisterForm, self).save(commit=False)
        user.set_password(self.cleaned_data['password'])
        user.save()
        avatar = self.cleaned_data['avatar']
        if avatar is not None:
            models.Profile(rating=0, user=user, avatar=avatar).save()
        else:
            models.Profile(rating=0, user=user, avatar='uploads/kot.jpg').save()
        return user

class AskForm(forms.ModelForm):
    title = forms.CharField(label='Title', max_length=30, widget=forms.TextInput(attrs={'placeholder': 'Title'}))
    text = forms.CharField(label='Text', widget=forms.Textarea)
    tags = forms.CharField(label='Tags',  max_length=30, widget=forms.TextInput(attrs={'placeholder': '"tag1", "tag2"'}))
    class Meta:
        model = Question
        fields = ['title', 'text', 'tags']
    def clean_tags(self):
        tags = self.cleaned_data['tags']
        tags_list = tags.strip().split(',')
        for tag in tags_list:
            print(tag)
        if len(tags_list) > 3:
            raise forms.ValidationError('Too many tags(maximum is 3)')
        if len(tags_list) != len(set(tags_list)):
            raise forms.ValidationError('All tags must be unique')
        return tags
    def save(self, commit=True, author=None):
        question = super(AskForm, self).save(commit=False)
        question.author = author
        question.created_at = datetime.now()
        question.updated_at = datetime.now()
        question.avatar = author.avatar
        question.rating = 0
        question.answers_count = 0
        question.save()
        for tag in self.cleaned_data['tags'].strip().split(','):
            if len(models.Tag.objects.filter(title=tag).all()) == 0:
                new_tag = models.Tag(title=tag)
                new_tag.save()
            else:
                new_tag = models.Tag.objects.get(title=tag)
            new_tag.question_set.add(question)
        return question

class AnswerForm(forms.ModelForm):
    text = forms.CharField(label='Your answer', widget=forms.Textarea)
    class Meta:
        model = Answer
        fields = ['text']
    def save(self, commit=True, author=None, question=None):
        answer = super(AnswerForm, self).save(commit=False)
        answer.author = author
        answer.avatar = author.avatar
        answer.created_at = datetime.now()
        answer.updated_at = datetime.now()
        answer.rating = 0
        answer.question = question
        answer.save()
        question.answers_count+=1
        question.save(update_fields=['answers_count'])
        return answer

class SettingsForm(forms.ModelForm):
    username = forms.CharField(label='Username', max_length=50, required=False, widget=forms.TextInput(attrs={'placeholder': 'new username'}))
    email = forms.CharField(label='Email', max_length=50, required=False, widget=forms.TextInput(attrs={'placeholder': 'new email'}))
    avatar = forms.ImageField(label='new avatar', required=False)

    class Meta:
        model = User
        fields = ['username', 'email', 'avatar']

    def save(self, commit=True, user=None):
        new_username = self.cleaned_data['username']
        new_email = self.cleaned_data['email']
        new_avatar = self.cleaned_data['avatar']
        if new_username != '' and new_username != user.username:
            user.username = new_username
        if new_email != '' and new_email != user.email:
            user.email = new_email
        profile = user.profile
        if new_avatar != '' and new_avatar != profile.avatar:
            profile.avatar = new_avatar
        user.save(update_fields=['username', 'email'])
        profile.save(update_fields=['avatar'])
        return user
