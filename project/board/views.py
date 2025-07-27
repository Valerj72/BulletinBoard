from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.mail import send_mail
from django.shortcuts import redirect
from django.views.generic import TemplateView, UpdateView, CreateView, ListView, DetailView
from  django.conf import global_settings
from .forms import ArticleForm, UserResponseForm
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

    def post(self, request, *args, **kwargs):
        article = self.get_object()
        form = UserResponseForm(request.POST)
        if form.is_valid():
            user_response = form.save(commit=False)
            user_response.author = self.request.user
            user_response.article = article
            user_response.save()
            send_mail(
                subject='Новый отклик на ваше объявление',
                message=f'Привет, {article.author.username}, на ваше объявление был оставлен отклик "{user_response.text}"',
                from_email=global_settings.DEFAULT_FROM_EMAIL,
                recipient_list=[article.author.email],
            )
            return redirect('article_detail', pk=article.pk)
        return self.render_to_response(self.get_context_data(form=form))

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = UserResponseForm()
        return context
