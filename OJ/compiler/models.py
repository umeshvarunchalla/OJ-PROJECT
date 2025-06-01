from django.db import models
from uuid import uuid4
from home.models import Problem
from django.contrib.auth.models import User
# Create your models here.
class Submission(models.Model):
    submission_id=models.CharField(max_length=100, default=uuid4, primary_key=True)
    problem=models.ForeignKey(Problem, on_delete=models.CASCADE)
    user=models.ForeignKey(User, on_delete=models.CASCADE)
    code=models.TextField()
    language=models.CharField(max_length=100)
    input=models.TextField()
    output=models.TextField()
    expected_output=models.TextField(blank=True, null=True)
    status=models.CharField(max_length=100)
    time=models.CharField(max_length=100)

class Testcase(models.Model):
    problem=models.ForeignKey(Problem, on_delete=models.CASCADE)
    input=models.TextField()
    output=models.TextField()