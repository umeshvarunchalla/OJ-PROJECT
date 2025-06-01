from django.urls import path
from .views import *
urlpatterns = [
    path('submit_page/<str:problem_id>',submit_page, name='submit_page'),
    path('submission/<str:submission_id>',submission_page, name='submission_page'),
    path('add_testcase/<str:problem_id>',add_testcase, name='add_testcase'),
]