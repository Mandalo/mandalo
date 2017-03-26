from django.contrib import admin

# Register your models here.
from .models import Submission, Assignment

admin.site.register(Submission)
admin.site.register(Assignment)
