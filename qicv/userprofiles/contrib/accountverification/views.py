# -*- coding: utf-8 -*-
from django.shortcuts import render

from userprofiles import settings as up_settings
from userprofiles.contrib.accountverification.models import AccountVerification


def registration_activate(request, activation_key):
    activation_key = activation_key.lower()
    account = AccountVerification.objects.activate_user(activation_key)

    return render(request, 'userprofiles/registration_activate.html', {
        'account': account,
        'expiration_days': up_settings.ACCOUNT_VERIFICATION_DAYS
    })


def registration_authorize(request, user):
    account = AccountVerification.objects.authorize_user(user)
    # if not account, it didn't work
    return render(request, 'userprofiles/registration_authorize.html', {
        'account': account,
    })
