from django import forms
from accounts.models import Profile

from userprofiles.forms import RegistrationForm

class ProfileRegistrationForm(RegistrationForm):
    about = forms.CharField(widget=forms.Textarea)

    def save_profile(self, new_user, *args, **kwargs):
        Profile.objects.create(
            user=new_user,
            about=self.cleaned_data['about']
        )

