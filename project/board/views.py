from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.mail import send_mail
from django.shortcuts import redirect
from django.views.generic import UpdateView, CreateView, ListView, DetailView
from  django.conf import settings
from .forms import ArticleForm, UserResponseForm
from .models import User, Article, UserResponse
from .filters import ResponseFilters

class ProfileView(LoginRequiredMixin, ListView):

    def __init__(self):
        super().__init__()
        self.filterset = None


    model = UserResponse
    template_name = 'flatpages/index.html'
    context_object_name = 'responses'

    def get_queryset(self):
        queryset = super().get_queryset().filter(article__author=self.request.user)
        self.filterset = ResponseFilters(self.request.GET, queryset=queryset, request=self.request.user)
        return self.filterset.qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['filterset'] = self.filterset
        return context


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
                from_email=settings.DEFAULT_FROM_EMAIL,
                recipient_list=[article.author.email],
            )
            return redirect('article_detail', pk=article.pk)
        return self.render_to_response(self.get_context_data(form=form))

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = UserResponseForm()
        return context


def response_accept(request, pk):
    response = UserResponse.objects.get(pk=pk)
    response.status = True
    response.save()
    send_mail(
        subject='Изменение статуса отклика',
        message='Ваш отклик был принят автором объявления!',
        from_email=settings.DEFAULT_FROM_EMAIL,
        recipient_list=[response.author.email],
    )
    return redirect('/')

def response_delete(request, pk):
    UserResponse.objects.get(pk=pk).delete()
    return redirect('/')

