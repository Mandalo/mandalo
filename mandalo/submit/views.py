from django.contrib import messages
from django.http import HttpResponseRedirect, Http404
from django.shortcuts import render  # , render_to_response

from .models import Assignment, Submission, Language
from .forms import UploadFileForm
from django.core.urlresolvers import reverse

import os
import subprocess
import shutil


def index(request):
    return render(request, "submit/landing.html", {})


def view_assign(request):
    assign_list = Assignment.objects.order_by('created_date')

    context = {"assign_list": assign_list, "pwd": os.getcwd()}
    page = render(request, 'submit/view_assign.html', context=context)
    return page


def view_submission(request, email, assignment):
    context = {}
    email = email + '@go.olemiss.edu'
    assignment_key = Assignment.objects.filter(name=assignment)

    if not assignment_key:
        raise Http404()

    assignment_key = assignment_key[0]
    sub = Submission.objects.filter(email=email).filter(assignment=assignment_key)
    if not sub:
        raise Http404()

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
    context['output'] = sub[0].result
    context['expected'] = assignment_key.expected_result + "\n"
    return render(request, "submit/view_submission.html", context=context)



def upload(request):
    if request.method == 'POST':
        form = UploadFileForm(request.POST, request.FILES)
        if form.is_valid():
            assignment = request.POST['assignment']
            email = request.POST['email'] + "@go.olemiss.edu"
            lang = request.POST['lang']
            lang_obj = Language.objects.filter(name=lang)[0]
            files = request.FILES.getlist('files')
            upload_dir, fpath_list = handle_uploaded_files(assignment, email, files)
            src_files = ';'.join(fpath_list)

            assignment_key = Assignment.objects.filter(
                name=assignment)[0]

            sub = Submission.objects.filter(email=email).filter(assignment=assignment_key)

            # if Submission already create, update. Else update
            if sub:
                sub = sub[0]
                base_dir = '../uploads'
                remove_dir = os.path.join(base_dir, assignment, email)
                shutil.rmtree(remove_dir)

            fname_list = handle_uploaded_files(assignment, email, files)

            if sub:
                sub.src_files=src_files
                sub.language=lang_obj
                sub.save()
            else:
                sub = Submission(
                    email=email, src_files=src_files,
                    result="", assignment=assignment_key,
                    language=lang_obj
                )
                sub.save()
            url = reverse('view_submission', kwargs={'email': email[:email.find('@')], 'assignment': assignment})

            lang_name = lang_obj.name
            lang_cmd = lang_obj.cmd
            lang_max_exec = lang_obj.max_exec_time
            lang_max_mem = lang_obj.max_mem_usage_KB

            job_spec = {
                'language': {
                    'name': lang_name,
                    'cmd': lang_cmd,
                    'max_exec_time': lang_max_exec,
                    'max_mem_usage_KB': lang_max_mem
                },
                'email': email,
                'src_files': src_files,
                'upload_dir': upload_dir,
            }

            out, err = run(job_spec)
            handle_run(sub, out, err)

            return HttpResponseRedirect(url)
        else:
            messages.error(request, "Error")
    else:
        form = UploadFileForm()

    assign_list = Assignment.objects.order_by('created_date')
    assign_list = [a.name for a in assign_list]

    lang_list = Language.objects.order_by('name')
    lang_list = [l.name for l in lang_list]

    context = {'assign_list': assign_list, 'form': form, 'lang_list': lang_list}

    return render(request, 'submit/upload.html', context)


def handle_uploaded_files(assignment, email, files):
    base_upload_dir = '../uploads'
    upload_dir = os.path.join(base_upload_dir, assignment, email)
    os.makedirs(upload_dir, exist_ok=True)

    fpath_list = []
    for f in files:
        fname = f.name
        fpath_list.append(os.path.join(upload_dir, fname))
        with open(fpath_list[-1], 'wb+') as destination:
            for chunk in f.chunks():
                destination.write(chunk)

    return upload_dir, fpath_list


def run(job_spec):
    upload_dir = job_spec['upload_dir']

    lang_dict = job_spec['language']
    lang_name = lang_dict['name']
    cmd_template = lang_dict['cmd']
    max_exec = lang_dict['max_exec_time']
    max_mem = lang_dict['max_mem_usage_KB']

    user_email = job_spec['email']
    src_files = job_spec['src_files'].split(';')
    fnames = list(map(lambda s: os.path.join("/code", os.path.basename(s)), src_files))

    cmd_list = cmd_template.split(';')
    cmd = " && ".join(map(lambda c: c + " " + " ".join(fnames), cmd_list))

    docker_cmd = "docker run -v %s:/code python_manager %s" % \
            (os.path.abspath(upload_dir), cmd)

    print(docker_cmd)
    print()

    p = subprocess.Popen(docker_cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    out, err = p.communicate()
    return out, err


def handle_run(sub, out, err):
    print("test")
    print(out)
    sub.complete = True
    sub.result = err if err else out
    sub.save()
    return
