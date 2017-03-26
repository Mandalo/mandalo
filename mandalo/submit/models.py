from django.db import models


class Language(models.Model):
    name = models.CharField(max_length=20)
    cmd = models.CharField(max_length=100)
    max_exec_time = models.IntegerField()
    max_mem_usage_KB = models.IntegerField()


class Assignment(models.Model):
    name = models.CharField(max_length=20)
    language = models.ForeignKey(Language, on_delete=models.CASCADE)
    created_date = models.DateTimeField(auto_now=True)
    due_date = models.DateField('Due Date')
    prompt = models.CharField(max_length=1000)
    expected_result = models.CharField(max_length=2000, null=True)


class Submission(models.Model):
    submitted_date = models.DateTimeField(auto_now=True)
    email = models.EmailField()
    src_files = models.CharField(max_length=2000)
    main_file = models.CharField(max_length=100, null=True)
    result = models.CharField(max_length=2000)
    assignment = models.ForeignKey(Assignment, on_delete=models.CASCADE)
    language = models.ForeignKey(Language, on_delete=models.CASCADE)
    complete = models.BooleanField(default=False)
    completed_date = models.DateTimeField(blank=True, null=True)
