from django.db import models


class Assignment(models.Model):
    lan = (
        ('Python', 'python'),
        ('Java', 'java'),
        ('C', 'C')
    )
    name = models.CharField(max_length=20)
    language = models.CharField(max_length=20, choices=lan)
    created_date = models.DateTimeField(auto_now=True)
    due_date = models.DateField('Due Date')
    prompt = models.CharField(max_length=1000)


class Submission(models.Model):
    submitted_date = models.DateTimeField(auto_now=True)
    email = models.EmailField()
    src_files = models.CharField(max_length=2000)
    result = models.CharField(max_length=2000)
    assignment = models.ForeignKey(Assignment, on_delete=models.CASCADE)
    language = models.CharField(max_length=2000)
