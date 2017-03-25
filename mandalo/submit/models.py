from django.db import models



class Assigment(models.Model):
    name = models.CharField(max_length=20)
    language = models.CharField(max_length=20)
    due_date = models.DateField()

class Submission(models.Model):
    email = models.EmailField()
    src_files = models.CharField(max_length=2000)
    result = models.CharField(max_length=2000)
    assigment = models.ForeignKey(Assigment  , on_delete=models.CASCADE)
    language = models.CharField(max_length=2000)
