from django_filters import FilterSet
from .models import UserResponse, Article


class ResponseFilters(FilterSet):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.user = kwargs.pop('request')
        self.filters['article'].queryset = Article.objects.filter(author=self.user)


    class Meta:
        model = UserResponse
        fields = ['article']
