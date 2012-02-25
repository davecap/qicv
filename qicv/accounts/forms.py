from django import forms
from accounts.models import UserProfile

from userprofiles.forms import RegistrationForm

class UserProfileRegistrationForm(RegistrationForm):
    about = forms.CharField(widget=forms.Textarea)

    def save_profile(self, new_user, *args, **kwargs):
        UserProfile.objects.create(
            user=new_user,
            about=self.cleaned_data['about']
        )

