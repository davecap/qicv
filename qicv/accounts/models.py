from django.db import models
from django.contrib.auth.models import User

from userprofiles.contrib.accountverification.models import AccountVerification


class UserProfile(models.Model):
    user = models.OneToOneField(User)
    about = models.TextField(blank=True)

    _verification = None

    def is_active(self):
        if self._verification is None:
            try:
                verification = AccountVerification.objects.get(user=self.user)
            except AccountVerification.DoesNotExist:
                return False
            else:
                self._verification = verification
        return self._verification.is_active()

    def is_authorized(self):
        if self._verification is None:
            try:
                verification = AccountVerification.objects.get(user=self.user)
            except AccountVerification.DoesNotExist:
                return False
            else:
                self._verification = verification
        return self._verification.is_authorized()

from django.dispatch import receiver
from django.db.models.signals import post_save


@receiver(post_save, sender=User, dispatch_uid="accounts.models")
def create_profile(sender, instance, created, **kwargs):
    """Create a matching profile whenever a user object is created."""
    if created:
        profile, new = UserProfile.objects.get_or_create(user=instance)
