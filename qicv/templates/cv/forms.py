from django import forms

from cv.models import CV


class CVCreateForm(forms.ModelForm):
    class Meta:
        model = CV

    def __init__(self, *args, **kwargs):
        super(CVCreateForm, self).__init__(*args, **kwargs)
        self.fields['user'] = forms.HiddenInput()
