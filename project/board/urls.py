from django.urls import path

from .views import ArticleCreate, ArticleList, ArticleDetail, ConfirmUser, response_accept, response_delete

urlpatterns = [
    path('confirm_user/', ConfirmUser.as_view(), name='confirm_user'),
    path('create/', ArticleCreate.as_view(), name='article_create'),
    path('', ArticleList.as_view(), name='article_list'),
    path('<int:pk>/', ArticleDetail.as_view(), name='article_detail'),
    path('response/<int:pk>/accept/', response_accept, name='response_accept'),
    path('response/<int:pk>/delete/', response_delete, name='response_delete'),
]