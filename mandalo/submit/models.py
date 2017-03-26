from django.db import models


class Assignment(models.Model):
    name = models.CharField(max_length=20)
    language = models.CharField(max_length=20)
    created_date = models.DateTimeField()
    due_date = models.DateField()
    prompt = models.CharField(max_length=1000)


class Submission(models.Model):
    submitted_date = models.DateTimeField()
    email = models.EmailField()
    src_files = models.CharField(max_length=2000)
    result = models.CharField(max_length=2000)
    assigment = models.ForeignKey(Assigment, on_delete=models.CASCADE)
    language = models.CharField(max_length=2000)
