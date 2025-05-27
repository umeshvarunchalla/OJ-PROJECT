from django.urls import path
from .views import *
urlpatterns=[
    path('home/',home, name='home'),
    path('problem/<str:problem_id>/', problem_detail, name='problem_detail'),
    path('addproblem/',add_problem, name='add_problem'),
    path('submission_history/', submission_history, name='submission_history'),
]