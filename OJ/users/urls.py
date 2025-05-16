from django.urls import path
from .views import login, signup, home

urlpatterns=[
    path('login/', login, name='login'),
    path('signup/', signup, name='signup'),
    path('home/', home, name='home'),
]