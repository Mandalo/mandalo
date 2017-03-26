from django.shortcuts import render
from .models import Assignment


def index(request):
    return render(request, "submit/landing.html", {})
    # return HttpResponse("Hello, world. You're at the polls index.")


def view_assign(request):
    assign_list = Assignment.objects.order_by('created_date')

    context = {"assign_list": assign_list}
    page = render(request, 'submit/view_assign.html', context=context)




