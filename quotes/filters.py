import django_filters

import django_filters
from django import forms
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
        method='collect_likes_order'
    )
    
    dislikes_order = django_filters.ChoiceFilter(
        field_name='dislikes',
        choices=(('asc', 'По возрастанию'), ('desc', 'По убыванию')),
        method='collect_dislikes_order'
    )
    
    views_order = django_filters.ChoiceFilter(
        field_name='views',
        choices=(('asc', 'По возрастанию'), ('desc', 'По убыванию')),
        method='collect_views_order'
    )
    
    date_from = django_filters.DateFilter(field_name='created_at', label='Дата добавления (начало)', lookup_expr='gte', widget=forms.DateInput(attrs={"type": "date"}))
    date_to = django_filters.DateFilter(field_name='created_at', label='Дата добавления (конец)', lookup_expr='lte', widget=forms.DateInput(attrs={"type": "date"}))
    
    limit = django_filters.NumberFilter(label='Число значений', method='collect_limit')

    class Meta:
        model = Quote
        fields = ["likes_order", "dislikes_order", "views_order", "date_from", "date_to", "limit"]
    
    def __init__(self, data=None, queryset=None, *, request=None, prefix=None):
        super().__init__(data=data, queryset=queryset, request=request, prefix=prefix)
        self._collected_ordering = []
        self._limit = None 

    def collect_likes_order(self, queryset, name, value):
        if value:
            self._collected_ordering.append("likes" if value == "asc" else "-likes")
        return queryset

    def collect_dislikes_order(self, queryset, name, value):
        if value:
            self._collected_ordering.append("dislikes" if value == "asc" else "-dislikes")
        return queryset

    def collect_views_order(self, queryset, name, value):
        if value:
            self._collected_ordering.append("views" if value == "asc" else "-views")
        return queryset
    
    def collect_limit(self, queryset, name, value):
        if value is not None and value > 0:
            self._limit = int(value)
        return queryset

    def filter_queryset(self, queryset):
        qs = super().filter_queryset(queryset)

        if self._collected_ordering:
            qs = qs.order_by(*self._collected_ordering)

        if self._limit:
            qs = qs[:self._limit]

        return qs
