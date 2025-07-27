import random
from string import hexdigits
from allauth.account.forms import SignupForm
from django.conf import settings
from django.core.mail import send_mail
from django.forms import ModelForm, Textarea

from .models import Article, UserResponse


class UserSignupForm(SignupForm):
    def save(self, request):
        user = super().save(request)
        user.is_active = False
        code = "".join(random.sample(hexdigits, 10))
        user.code = code
        user.save()
        send_mail(
            subject='Подтверждение регистрации!',
            message=f'Подтвердите регистрацию по коду: {code}',
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[user.email],
        )
        return user


class ArticleForm(ModelForm):
    class Meta:
        model = Article
        fields = ('title', 'text', 'category')


class UserResponseForm(ModelForm):
    class Meta:
        model = UserResponse
        fields = ('text',)
        widgets = {'text': Textarea(attrs={'class': 'form-text', 'cols': 70, 'rows': 3})}
