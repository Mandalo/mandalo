from django.contrib import admin

# Register your models here.
from .models import Submission, Assignment, Language

admin.site.register(Submission)
admin.site.register(Assignment)
admin.site.register(Language)
