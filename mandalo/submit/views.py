from django.contrib import messages
from django.http import HttpResponseRedirect, Http404
from django.shortcuts import render  # , render_to_response

from .models import Assignment
from .models import Submission
from .forms import UploadFileForm

import os


def index(request):
    return render(request, "submit/landing.html", {})
    # return HttpResponse("Hello, world. You're at the polls index.")


def view_assign(request):
    assign_list = Assignment.objects.order_by('created_date')

    context = {"assign_list": assign_list, "pwd": os.getcwd()}
    page = render(request, 'submit/view_assign.html', context=context)
    return page


def view_submission(request, email, assignment):
    context = {}
    email = email + '@go.olemiss.edu'
    assignment_key = Assignment.objects.filter(
        name=assignment)
    if not assignment_key:
        return Http404()
    assignment_key = assignment_key[0]
    sub = Submission.objects.filter(email=email).filter(assignment=assignment_key)
    if not sub:
        return Http404()
    context['name'] = assignment_key.name
    context['prompt'] = assignment_key.prompt
    files = sub[0].src_files.split(';')
    string_files = []
    for file in files:
        f = open(file, 'r+')
        name = f.name[f.name.rfind('/')+1:]
        string_files.append((name, f.read()))
        f.close()
    context['files'] = string_files
    return render(request, "submit/view_submission.html", context=context)



def upload(request):
    # c = {}
    # c.update(csrf(request))

    if request.method == 'POST':
        form = UploadFileForm(request.POST, request.FILES)
        if form.is_valid():
            assignment = request.POST['assignment']
            email = request.POST['email']
            lang = request.POST['lang']
            files = request.FILES.getlist('files')
            fname_list = handle_uploaded_files(assignment, email, files)

            assignment_key = Assignment.objects.filter(
                name=assignment)[0]

            sub = Submission(
                email=email, src_files=';'.join(fname_list),
                result="", assignment=assignment_key,
                language=lang
            )
            sub.save()

            return HttpResponseRedirect('/test')
        else:
            messages.error(request, "Error")
    else:
        form = UploadFileForm()

    return render(request, 'submit/upload.html', {'form': form})


def handle_uploaded_files(assignment, email, files):
    base_upload_dir = '../uploads'
    upload_dir = os.path.join(base_upload_dir, assignment, email)
    os.makedirs(upload_dir, exist_ok=True)

    fname_list = []
    for f in files:
        fname = f.name
        fname_list.append(os.path.join(upload_dir, fname))
        with open(fname_list[-1], 'wb+') as destination:
            for chunk in f.chunks():
                destination.write(chunk)

    return fname_list
