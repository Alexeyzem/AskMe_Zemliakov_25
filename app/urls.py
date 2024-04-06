from django.urls import path

from app import views

urlpatterns = [
    path('', views.index, name='index'),
    path('hot/', views.hot, name='hot'),
    path('questions/<int:question_id>', views.question, name='question'),
    path('ask/', views.new_question, name='new_question'),
    path('tag/<str:tag_title>', views.tags, name='tags'),
    path('settings/', views.settings, name='settings'),
    path("logout/", views.log_out, name='logout'),
    path("signup/", views.sign_up, name='signup'),
    path("members/", views.members, name='members'),
    path("login/", views.login, name='login')
]