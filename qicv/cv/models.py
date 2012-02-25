from django.db import models
from django.contrib.auth.models import User
from django.utils.translation import ugettext as _


class CV(models.Model):
    user = models.OneToOneField(User)
    first_name = models.CharField(_("First name"), max_length=50)
    last_name = models.CharField(_("Last name"), max_length=50)
    location = 
    date_of_birth
    # photo
