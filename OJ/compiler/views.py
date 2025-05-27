from django.shortcuts import render,redirect
from django.http import HttpResponse
from django.template import loader
from home.models import Problem
from .models import Submission
from .templates import *
from django.contrib.auth.decorators import login_required
from django.contrib import messages
# Create your views here.
@login_required
def submit_page(request, problem_id):
    if request.method=='POST':
        code = request.POST.get('code')
        language = request.POST.get('language')
        input_data = request.POST.get('input')
        problem = Problem.objects.get(problem_id=problem_id)
        if not code:
            messages.error(request, 'Code is required.')
            return redirect('submit_page', problem_id=problem_id)
        else:
            output =run_code(code, language, input_data)
            submission = Submission(
                problem=problem,
                user=request.user,
                code=code,
                language=language,
                input=input_data,
                output=output,
                expected_output='',
                status='Pending',
                time='0'
            )
            if output == "Compilation Error":
                submission.status = "Compilation Error"
            elif output == "Runtime Error":
                submission.status = "Runtime Error"
            else:
                submission.status = "Accepted"
            submission.save()
            return redirect('submission_page', submission_id=submission.submission_id)
    template = loader.get_template('submit_page.html')
    problem=Problem.objects.get(problem_id=problem_id)
    context = {
        'problem_title': problem.problem_title,
    }
    return HttpResponse(template.render(context, request))

@login_required
def submission_page(request, submission_id):
    submission=Submission.objects.get(submission_id=submission_id)
    problem=Problem.objects.get(problem_id=submission.problem.problem_id)
    template = loader.get_template('submission_page.html')
    context={
        'problem_id': problem.problem_id,
        'problem_title': problem.problem_title,
        'submission_id': submission.submission_id,
        'code': submission.code,
        'input': submission.input,
        'output': submission.output,
        'expected_output': submission.expected_output,
        'language': submission.language,
        'status': submission.status,
        'time': submission.time,
    }
    return HttpResponse(template.render(context, request))

from pathlib import Path
import subprocess
from django.conf import settings
import uuid
def run_code(code, language, input_data):
    proj_dir=Path(settings.BASE_DIR)
    directories=['codes','inputs','outputs']
    for directory in directories:
        dir_path = proj_dir / directory
        if not dir_path.exists():
            dir_path.mkdir(parents=True, exist_ok=True)
    
    unique_name=str(uuid.uuid4())
    code_dir=f"{unique_name}.{language}"
    input_dir=f"{unique_name}.txt"
    output_dir=f"{unique_name}_output.txt"

    code_path = proj_dir / 'codes' / code_dir
    input_path = proj_dir / 'inputs' / input_dir
    output_path = proj_dir / 'outputs' / output_dir

    with open(code_path, 'w') as code_file:
        code_file.write(code)
    
    with open(input_path, 'w') as input_file:
        input_file.write(input_data)

    with open(output_path, 'w') as output_file:
        pass #empty file for output

    if language=='C++':
        executable= f"{proj_dir}/codes/{unique_name}.out"
        compiling = subprocess.run(['g++', code_path, '-o', executable])
        if compiling.returncode != 0:
            return "Compilation Error"
        else:
            with open(input_path, 'r') as input_file:
                process = subprocess.run([executable], stdin=input_file, stdout=output_file)
                if process.returncode != 0:
                    return "Runtime Error"
    elif language=='C':
        executable = f"{proj_dir}/codes/{unique_name}.out"
        compiling = subprocess.run(['gcc', code_path, '-o', executable])
        if compiling.returncode != 0:
            return "Compilation Error"
        else:
            with open(input_path, 'r') as input_file:
                process = subprocess.run([executable], stdin=input_file, stdout=output_file)
                if process.returncode != 0:
                    return "Runtime Error"
    elif language=='python':
        with open(input_path, 'r') as input_file:
            with open(output_path, 'w') as output_file:
                process = subprocess.run(['python', code_path], stdin=input_file, stdout=output_file)
                if process.returncode != 0:
                    return "Runtime Error"
    with open(output_path, 'r') as output_file:
        output = output_file.read()
    return output