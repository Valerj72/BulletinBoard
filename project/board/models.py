from django.db import models
from django.contrib.auth.models import User
from ckeditor.fields import RichTestField

# Create your models here.
class Article(models.Model):
    TIPE = (
        ('tank', 'Танки'),
        ('heals', 'Хилы'),
        ('dd', 'ДД'),
        ('buyers', 'Торговцы'),
        ('gildemaster', 'Гилдмастеры'),
        ('quest', 'Квестгиверы'),
        ('smith', 'Кузнецы'),
        ('tanner', 'Кожевники'),
        ('potion', 'Зельевары'),
        ('spellmaster', 'Мастера заклинаний'),
    )
    author = models.OneToOneField(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=64)
    category = models.CharField(max_length=16, choices=TIPE, default='tank')
    text = RichTestField()


class UserResponse(models.Model):
    author = models.OneToOneField(User, on_delete=models.CASCADE)
    text = models.TextField()
    article = models.ForeignKey(Article, on_delete=models.CASCADE)
    status = models.BooleanField(default=False)


class NewUser(User):
    status = models.BooleanField(default=False)
    auth_code = models.CharField(max_length=128)
