from django.urls import path

from .views import ConfirmUser

urlpatterns = [
    path('confirm_user/', ConfirmUser.as_view(), name='confirm_user'),

]