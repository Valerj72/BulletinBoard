import random
from string import hexdigits
from allauth.account.forms import SignupForm
from django.conf import settings
from django.core.mail import send_mail




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