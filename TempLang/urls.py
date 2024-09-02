from django.urls import path
from . import views


urlpatterns =[
    path('', views.home_view, name='home'),
    path('login', views.login_view, name='login'),
    path('register', views.register_view, name='register'),
    path('logout', views.logout_view, name='logout'),
    path('todos', views.todos_view, name='todos'),
    path('todos/all', views.all_todos_view, name='alltodos'),
    path('todos/<int:pk>', views.one_todo_view, name='todo'),
    path('todos/<int:pk>/<str:act>', views.todo_action_view, name='todo_act'),
]