from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver
from django.core.mail import send_mail
from .models import UserResponse
from django.contrib.auth.models import User


@receiver(pre_save, sender=UserResponse)
def my_handler(sender, instance, created, **kwargs):
    if instance.status:
        mail = instance.author.email
        send_mail(
        'Subject here',
        'Here is the message.',
        'host@mail.ru',
        [mail],
        fail_silently=False,
        )
    mail = instance.article.author.email
    send_mail(
        'Subject here',
        'Here is the message.',
        'host@mail.ru',
        [mail],
        fail_silently=False,
    )
