import django_filters
from .models import Quote

import django_filters
from django.db.models import F
from .models import Quote

class QuoteFilter(django_filters.FilterSet):
    """
    Фильтрация списка цитат по числу лайков/дизлайков, просмотрам, дате создания
    
    Attributes:
        likes_order(ChoiceFilter): Фильтрация по числу лайков (по убыванию/возрастанию)
        dislikes_order(ChoiceFilter): Фильтрация по числу дизлайков (по убыванию/возрастанию)
        views_order(ChoiceFilter): Фильтрация числу просмотров (по убыванию/возрастанию)
        date_from(DateFilter): Фильтрация по дате начала периода (>=)
        date_to(DateFilter): Фильтрация по дате окончания периода (<=)
        limit(NumberFilter): Фильтрация числа отображаемых значений на странице
    """
    
    likes_order = django_filters.ChoiceFilter(
        field_name='likes',
        choices=(('asc', 'По возрастанию'), ('desc', 'По убыванию')),
        method='filter_likes_order'
    )
    
    dislikes_order = django_filters.ChoiceFilter(
        field_name='dislikes',
        choices=(('asc', 'По возрастанию'), ('desc', 'По убыванию')),
        method='filter_dislikes_order'
    )
    
    views_order = django_filters.ChoiceFilter(
        field_name='views',
        choices=(('asc', 'По возрастанию'), ('desc', 'По убыванию')),
        method='filter_views_order'
    )
    
    date_from = django_filters.DateFilter(field_name='created_at', label='Дата добавления (начало)', lookup_expr='gte')
    date_to = django_filters.DateFilter(field_name='created_at', label='Дата добавления (конец)', lookup_expr='lte')
    
    limit = django_filters.NumberFilter(label='Число значений', method='filter_limit')

    class Meta:
        model = Quote
        fields = []

    def filter_likes_order(self, queryset, name, value):
        if value == 'asc':
            return queryset.order_by('likes')
        elif value == 'desc':
            return queryset.order_by('-likes')
        return queryset
    
    def filter_dislikes_order(self, queryset, name, value):
        if value == 'asc':
            return queryset.order_by('dislikes')
        elif value == 'desc':
            return queryset.order_by('-dislikes')
        return queryset

    def filter_views_order(self, queryset, name, value):
        if value == 'asc':
            return queryset.order_by('views')
        elif value == 'desc':
            return queryset.order_by('-views')
        return queryset

    def filter_limit(self, queryset, name, value):
        try:
            limit = int(value)
            return queryset[:limit]
        except (ValueError, TypeError):
            return queryset
