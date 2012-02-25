from django.db import models
from django.contrib.auth.models import User
from django.utils.translation import ugettext as _


class CV(models.Model):
    LIST_PRIVACY_CHOICES = (
        (u'hidden', _('Do not show in "All CVs"')),
        (u'limited', _('Show only initials and country in "All CVs"')),
        (u'none', _('Show full name and country in "All CVs"')),
    )

    PROFILE_PRIVACY_CHOICES = (
        (u'hidden', _('Require permission to access')),
        # (u'limited', _('Show limited profile to unauthorized users')),
        (u'none', _('Show full profile to all users')),
    )

    user = models.ForeignKey(User)
    first_name = models.CharField(_("First name"), max_length=50)
    last_name = models.CharField(_("Last name"), max_length=50)
    city = models.CharField(_("City"), max_length=50)
    country = models.ForeignKey('countries.Country')
    date_of_birth = models.DateField()
    list_privacy = models.CharField(_("List Privacy"), choices=LIST_PRIVACY_CHOICES, max_length=20, default="hidden")
    profile_privacy = models.CharField(_("Profile Privacy"), choices=PROFILE_PRIVACY_CHOICES, max_length=20, default="hidden")
    created = models.DateTimeField(_("Created On"), auto_now_add=True, blank=True, editable=False)
    updated = models.DateTimeField(_("Updated On"), auto_now=True, blank=True, editable=False)

    def __unicode__(self):
        return self.full_name()

    def initials(self):
        return '%s.%s.' % (self.first_name[0], self.last_name[0])

    def full_name(self):
        return ' '.join([self.first_name, self.last_name])

    def has_list_permission(self, user):
        """Check if a user has permission to view this profile"""
        if self.user == user:
            return True
        return self.list_privacy != 'hidden'

    def get_listable_info(self, user):
        if self.has_list_permission(user):
            if self.has_view_permission(user) or self.list_privacy == 'none':
                # get all listable info
                return {'can_view': self.has_view_permission(user), 'pk': self.pk, 'name': self.full_name(), 'country': self.country}
            elif self.list_privacy == 'limited':
                # limited info
                return {'can_view': self.has_view_permission(user), 'pk': self.pk, 'name': self.initials(), 'country': self.country}
        else:
            return None

    def has_view_permission(self, user):
        """Check if a user can view the profile"""
        if user.is_staff or self.user == user:
            return True

        try:
            perm = CVViewPermission.objects.get(user=user)
        except CVViewPermission.DoesNotExist:
            return False
        else:
            return perm.granted()

    def request_permission(self, user):
        """Called when a user requests permission to view this profile"""
        try:
            perm = CVViewPermission.objects.get(user=user)
        except CVViewPermission.DoesNotExist:
            # create it!
            perm = CVViewPermission(user=user,
                                    cv=self,
                                    status='requested')
            perm.save()
            # TODO: notify the owner of this CV
        else:
            return False


class CVViewPermission(models.Model):
    PERMISSION_STATUS_CHOICES = (
        (u'requested', 'Requested'),
        (u'granted', 'Granted'),
        (u'revoked', 'Revoked')
    )
    user = models.OneToOneField(User)
    cv = models.ForeignKey(CV, related_name='permissions')
    status = models.CharField(max_length=10, choices=PERMISSION_STATUS_CHOICES)

    def granted(self):
        return self.status == 'granted'
