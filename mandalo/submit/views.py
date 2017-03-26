from django.shortcuts import render
from django.http import HttpResponse
from django.template import RequestContext, loader

from .models import Assignment


def index(request):
    return render(request, "submit/landing.html", {})
    # return HttpResponse("Hello, world. You're at the polls index.")


def view_assgn(request):
    assign_list = Assignment.objects.order_by('created_date')
    text = "<br>".join(a.name for a in assign_list)
    template = loader.get_template('submit/view_assign.html')

    return HttpResponse(template.render(assign_list, request))
