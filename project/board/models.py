from django.db import models
from django.contrib.auth.models import AbstractUser
from ckeditor_uploader.fields import RichTextUploadingField
from django.urls import reverse


class User(AbstractUser):
    code = models.CharField(max_length=128, null=True, blank=True)

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
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    date_creation = models.DateTimeField(auto_now_add=True)
    title = models.CharField(max_length=64)
    category = models.CharField(max_length=16, choices=TIPE, default='tank')
    text = RichTextUploadingField()

    def get_absolute_url(self):
        return reverse('article_detail', kwargs={'pk': self.pk})


class UserResponse(models.Model):
    author = models.OneToOneField(User, on_delete=models.CASCADE)
    text = models.TextField()
    article = models.ForeignKey(Article, on_delete=models.CASCADE)
    status = models.BooleanField(default=False)



