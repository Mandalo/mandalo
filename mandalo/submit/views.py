from django.shortcuts import render
from .models import Assignment
from .forms import UploadFileForm


def index(request):
    return render(request, "submit/landing.html", {})
    # return HttpResponse("Hello, world. You're at the polls index.")


def view_assign(request):
    assign_list = Assignment.objects.order_by('created_date')

    context = {"assign_list": assign_list}
    page = render(request, 'submit/view_assign.html', context=context)
    return page

def upload(request):
    if request.method == 'POST':
        form = UploadFileForm(request.POST, request.FILES)
        if form.is_valid():
            handle_uploaded_file(request.FILES['file'])
            return HttpResponseRedirect('/success/url/')
    else:
        form = UploadFileForm()
    return render(request, 'submit/upload.html', {'form': form})
