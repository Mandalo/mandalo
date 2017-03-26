from django import forms

from .models import Assignment
import submit.const


class UploadFileForm(forms.Form):
    assign_list = Assignment.objects.order_by('created_date')
    assign_list = [a.name for a in assign_list]
    assign_choices = zip(
        assign_list,
        map(lambda s: s.replace(" ", "_"), assign_list)
    )


    assignment = forms.ChoiceField(choices=assign_choices)
    lang = forms.ChoiceField(choices=submit.const.lan)
    email = forms.EmailField()
    files = forms.FileField(widget=forms.ClearableFileInput(
        attrs={'multiple': True}))
