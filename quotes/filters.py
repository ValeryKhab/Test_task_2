import django_filters
from .models import Quote

import django_filters
from django.db.models import F
from .models import Quote

class QuoteFilter(django_filters.FilterSet):
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

    created_order = django_filters.ChoiceFilter(
        field_name='created_at',
        choices=(('asc', 'По возрастанию'), ('desc', 'По убыванию')),
        method='filter_created_order'
    )
    
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

    def filter_created_order(self, queryset, name, value):
        if value == 'asc':
            return queryset.order_by('created_at')
        elif value == 'desc':
            return queryset.order_by('-created_at')
        return queryset
    
    def filter_limit(self, queryset, name, value):
        try:
            limit = int(value)
            return queryset[:limit]
        except (ValueError, TypeError):
            return queryset
