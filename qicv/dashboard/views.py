from django.views.generic import TemplateView
from django.contrib import messages

class DashboardView(TemplateView):
    template_name = "dashboard/dashboard.html"

