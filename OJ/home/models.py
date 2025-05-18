from django.db import models
from django.contrib.auth.models import User
# Create your models here.
class Problem(models.Model):
    id=models.AutoField(primary_key=True)
    problem_id =models.CharField(max_length=50,unique=True)
    problem_title = models.CharField(max_length=100,unique=True)
    problem_description = models.TextField()
    problem_author=models.ForeignKey(User, on_delete=models.CASCADE)
    # def save(self,*args,**kwargs):
    #     if not self.problem_id:
    #         super().save(*args, **kwargs)
    #         self.problem_id = "P"+str(self.id)
    #     super().save(*args, **kwargs)