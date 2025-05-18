from django.shortcuts import render, redirect
from .models import Problem
from django.http import HttpResponse
from django.template import loader
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import ProblemForm
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
    return HttpResponse(f"Details of problem {problem_id}")

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