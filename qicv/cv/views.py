from django.views.generic import ListView, DetailView, FormView
from django.views.generic.base import View
from django.contrib import messages

from cv.models import CV
from cv.forms import CVCreateForm


class CVRequestView(View):
    pass


class AllCVListView(ListView):

    context_object_name = "cvs"
    # queryset = CV.objects.all(publisher__name="Acme Publishing")
    template_name = "cv/all.html"

    def get_queryset(self):
        cvs = CV.objects.all()
        cvs = [c.get_listable_info(self.request.user) for c in cvs if c.has_list_permission(self.request.user)]
        return cvs


class CVCreateView(FormView):
    template_name = "cv/create.html"
    form_class = CVCreateForm

    # def post(self, request, *args, **kwargs):
    #     # Process view when the form gets POSTed
    #     pass

    def get_initial(self):
        return {'user': self.request.user}

    def get_success_url(self):
        # Redirect to previous url
        return self.request.META.get('HTTP_REFERER', None)

    def form_valid(self, form):
        cv = form.save(commit=False)
        cv.user = self.request.user
        cv.save()
        messages.success(
            self.request,
            "You have successfully created a new CV."
        )
        return super(CVCreateView, self).form_valid(form)

    def form_invalid(self, form):
        messages.error(
            self.request,
            "Check the form and try again."
        )
        return super(CVCreateView, self).form_invalid(form)


class CVEditView(View):
    template_name = "cv/edit.html"


class MyCVListView(ListView):

    context_object_name = "cvs"
    # queryset = CV.objects.all(publisher__name="Acme Publishing")
    template_name = "cv/my.html"

    def get_queryset(self):
        cvs = CV.objects.filter(user=self.request.user)
        return cvs


class CVDetailView(DetailView):
    queryset = CV.objects.all()

    def get_object(self):
        # Call the superclass
        obj = super(CVDetailView, self).get_object()
        if obj.has_view_permission(obj):
            return obj
        else:
            return None
