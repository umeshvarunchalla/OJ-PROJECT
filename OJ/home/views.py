from django.shortcuts import render, redirect
from .models import Problem
from django.http import HttpResponse
from django.template import loader
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import ProblemForm
from .templates import *
from compiler.models import Submission
# Create your views here.
@login_required
def home(request):
    problems_list = list(Problem.objects.all())
    status_list=["unattempted" for _ in problems_list]
    submissions= Submission.objects.filter(user=request.user)
    for submission in submissions:
        problem_index= problems_list.index(submission.problem)
        if status_list[problem_index]== "unattempted":
            if submission.status == "Accepted":
                status_list[problem_index] = "solved"
            else:
                status_list[problem_index] = "attempted"
        elif status_list[problem_index] == "attempted":
            if submission.status == "Accepted":
                status_list[problem_index] = "solved"
    problems_list = zip(problems_list, status_list)
    context = {
        'combined_data': problems_list,
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
        'problem_author': problem.problem_author.username,
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
    statuses = [submission.status for submission in submissions]
    problem_ids = [submission.problem.problem_id for submission in submissions]
    problem_titles = [submission.problem.problem_title for submission in submissions]
    languages = [submission.language for submission in submissions]
    combined_data=zip(submission_ids,statuses, problem_ids, problem_titles, languages)
    context = {
        'combined_data':combined_data,
    }
    template = loader.get_template('submission_history.html')
    return HttpResponse(template.render(context, request))