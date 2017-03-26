from django import forms

from .models import Assignment, Language


class UploadFileForm(forms.Form):
    assign_list = Assignment.objects.order_by('created_date')
    assign_list = [a.name for a in assign_list]
    assign_choices = zip(
        assign_list,
        map(lambda s: s.replace(" ", "_"), assign_list)
    )

    lang_list = Language.objects.order_by('name')
    lang_list = [l.name for l in lang_list]
    lang_choices = zip(
        lang_list,
        map(lambda s: s.replace(" ", "_"), lang_list)
    )

    assignment = forms.ChoiceField(choices=assign_choices)
    lang = forms.ChoiceField(choices=lang_choices)
    email = forms.EmailField()
    files = forms.FileField(widget=forms.ClearableFileInput(
        attrs={'multiple': True}))
