from django.urls import path

from .views import ArticleCreate, ArticleList, ArticleDetail
from .views import ConfirmUser

urlpatterns = [
    path('confirm_user/', ConfirmUser.as_view(), name='confirm_user'),
    path('create/', ArticleCreate.as_view(), name='article_create'),
    path('', ArticleList.as_view(), name='article_list'),
    path('<int:pk>/', ArticleDetail.as_view(), name='article_detail'),
]