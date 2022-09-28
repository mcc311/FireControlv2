from email.policy import default
from unittest import result
from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator

# Create your models here.
class Problem(models.Model):
    id = models.AutoField(primary_key=True)
    def default_problem_request():
        return dict({"ships":[], 'distances':{}})
    problem_request = models.JSONField(default=default_problem_request)

    def default_results():
        return dict({"policy":[]})
    results = models.JSONField(default=default_results)

    def default_time_cost():
        return dict({"policy":0})
    # def defaultOptionsTemplate():
    #     return dict({"defaultWeapons":[],})
    # options = models.JSONField(blank=True, default=defaultOptionsTemplate)
    def __str__(self):
        return self.id