from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import redirect
from django.views.generic import TemplateView, UpdateView, CreateView, ListView, DetailView

from .forms import ArticleForm
from .models import User, Article


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


class ArticleCreate(LoginRequiredMixin, CreateView):
    model = Article
    form_class = ArticleForm
    template_name = 'article_create.html'

    def form_valid(self, form):
        article = form.save(commit=False)
        article.author = self.request.user
        article.save()
        return super().form_valid(form)


class ArticleList(ListView):
    model = Article
    context_object_name = 'articles'
    template_name = 'article_list.html'


class ArticleDetail(DetailView):
    model = Article
    context_object_name = 'article'
    template_name = 'article_detail.html'
