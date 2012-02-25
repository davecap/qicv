from django.forms import ModelForm

from cv.models import CV


class CVCreateForm(ModelForm):
    class Meta:
        model = CV
