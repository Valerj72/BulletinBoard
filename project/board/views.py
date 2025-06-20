from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import redirect
from django.views.generic import TemplateView, UpdateView

from .models import User


class ProfileView(LoginRequiredMixin, TemplateView):
    template_name = 'flatpages/index.html'


class ConfirmUser(UpdateView):
    model = User
    context_object_name = 'user'

    def post(self, request, *args, **kwargs):
        if 'code' in request.POST:
            code = request.POST['code']
            user = User.objects.filter(code=code)
            if user.exists():
                user.update(is_active=True)
                user.update(code=None)

        return redirect('account_login')
