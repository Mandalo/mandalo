from django.shortcuts import render
from django.http import HttpResponse

from .models import Assignment


def index(request):
    return render(request, "submit/landing.html", {})
    # return HttpResponse("Hello, world. You're at the polls index.")


def view_assgn(request):
    assign_list = Assignment.objects.order_by('created_date')
    text = "<br>".join(a.name for a in assign_list)
    return HttpResponse(text)
