from django.urls import path
from .views import index, todo, todo_archived, register_user, logout_user, login_user, create_action, to_archive, from_archive

urlpatterns = [
    path('', index, name='index'),
    path('todo/<slug:slug>', todo, name='todo'),
    path('archived', todo_archived, name='archive'),
    path('register', register_user, name='register'),
    path('logout', logout_user, name='logout'),
    path('login', login_user, name='login'),
    path('add', create_action, name='addtodo'),
    path('to_archive/<slug:slug>', to_archive, name='to_archive'),
    path('from_archive/<slug:slug>', from_archive, name='from_archive'),
]