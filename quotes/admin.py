from django.contrib import admin
from .models import Quote


@admin.register(Quote)
class QuoteAdmin(admin.ModelAdmin):
    """
    Admin-представление для модели цитаты
    """
    
    list_display = ("text", "source", "weight", "likes", "dislikes", "views", "created_at",)
    list_filter = ("source", "likes", "dislikes", "views", "created_at",)
    search_fields = ("text", "source",)
    ordering = ("-created_at",)
