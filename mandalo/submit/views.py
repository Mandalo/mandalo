from django.contrib import messages
from django.http import HttpResponseRedirect, Http404
from django.shortcuts import render  # , render_to_response

from .models import Assignment, Submission, Language
from .forms import UploadFileForm

import json
import os
import subprocess


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
    if request.method == 'POST':
        form = UploadFileForm(request.POST, request.FILES)
        if form.is_valid():
            assignment = request.POST['assignment']
            email = request.POST['email']
            lang = request.POST['lang']
            lang_obj = Language.objects.filter(name=lang)[0]
            files = request.FILES.getlist('files')
            upload_dir, fpath_list = handle_uploaded_files(assignment, email, files)
            src_files = ';'.join(fpath_list)

            assignment_key = Assignment.objects.filter(
                name=assignment)[0]

            sub = Submission(
                email=email, src_files=src_files,
                result="", assignment=assignment_key,
                language=lang_obj
            )
            sub.save()

            lang_name = lang_obj.name
            lang_cmd = lang_obj.cmd
            lang_max_exec = lang_obj.max_exec_time
            lang_max_mem = lang_obj.max_mem_usage_KB

            json_dict = {
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

            '''
            json_str = json.dumps(json_dict)

            #docker_cmd = "docker run -v %s:/code/src python_manager python " \
            #    "manager.py \"%s\"" % (os.path.abspath(upload_dir), json_str)
            docker_cmd = "docker run -v %s:/manager -v %s:/code python_manager " \
                    "python manager/manager.py '%s'" % \
                    (
                        os.path.abspath("../manager/manager/"),
                        os.path.abspath(upload_dir),
                        json_str
                    )

            p = subprocess.Popen(docker_cmd, shell=True, stdout=subprocess.PIPE)
            out, err = p.communicate()
            print(out)
            '''
            run(json_dict)

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
    #cmd = "ls"
    #sub_cmd = 'ulimit -t %d && %s' % (max_exec, cmd)

    docker_cmd = "docker run -v %s:/code python_manager %s" % \
            (os.path.abspath(upload_dir), cmd)

    print(docker_cmd)
    print()

    p = subprocess.Popen(docker_cmd, shell=True, stdout=subprocess.PIPE)
    out, err = p.communicate()
    print(out)
