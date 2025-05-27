from django.shortcuts import render, redirect
from .models import Problem
from django.http import HttpResponse
from django.template import loader
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import ProblemForm
from .templates import *
# Create your views here.
@login_required
def home(request):
    problems_list = Problem.objects.all()
    context = {
        'problems_list': problems_list,
    }
    template=loader.get_template('home.html')
    return HttpResponse(template.render(context, request))

@login_required
def problem_detail(request, problem_id):
    problem= Problem.objects.get(problem_id=problem_id)
    context = {
        'problem_title': problem.problem_title,
        'problem_description': problem.problem_description,
        'problem_id': problem.problem_id,
    }
    template=loader.get_template('problem_page.html')
    return HttpResponse(template.render(context, request))

@login_required
def add_problem(request):
    if request.method == 'POST':
        form=ProblemForm(request.POST)
        if form.is_valid():
            new_problem = form.save(commit=False)
            new_problem.problem_author = request.user
            new_problem.save()
            messages.success(request, 'Problem added successfully!')
            return redirect('home')
    else:
        form=ProblemForm()
    return render(request, 'add_problem.html', {'form': form})

from compiler.models import Submission
@login_required
def submission_history(request):
    submissions = Submission.objects.filter(user=request.user)
    submission_ids = [submission.submission_id for submission in submissions]
    context = {
        'submission_ids': submission_ids,
    }
    template = loader.get_template('submission_history.html')
    return HttpResponse(template.render(context, request))