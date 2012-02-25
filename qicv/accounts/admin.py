# -*- coding: utf-8 -*-
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User
from django.utils.translation import ugettext_lazy as _

from accounts.models import UserProfile
from userprofiles.contrib.accountverification.models import AccountVerification


class UserProfileInline(admin.StackedInline):
    model = UserProfile
    extra = 1
    max_num = 1


class CustomUserAdmin(UserAdmin):
    list_display = ('email', 'first_name', 'last_name', 'is_active', 'is_authorized', 'date_joined', 'is_staff', 'is_superuser',)
    actions = ['authorize_users', ]
    inlines = [UserProfileInline, ]

    def authorize_users(self, request, queryset):
        for user in queryset:
            if AccountVerification.objects.authorize_user(user=user):
                self.message_user(request, "User %s has been authorized." % (user.email))
            else:
                self.message_user(request, "User %s could not be authorized!" % (user.email))
    authorize_users.short_description = _("Authorize users")

    def is_authorized(self, obj):
        print obj
        profile = UserProfile.objects.get(user=obj)
        print profile
        return profile.is_authorized()
    is_authorized.boolean = True


admin.site.unregister(User)
admin.site.register(User, CustomUserAdmin)
admin.site.register(UserProfile)
