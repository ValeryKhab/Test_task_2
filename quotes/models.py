from django.db import models
from datetime import datetime
from django.core.exceptions import ValidationError
from django.core.validators import MinValueValidator, MaxValueValidator


class Quote(models.Model):
    """
    Модель цитаты

    Attributes:
        text(string): Текст цитаты
        source(string): Источник цитаты
        weight(int): Вес
        likes(int): Лайки
        dislikes(int): Дизлайки
        views(int): Просмотры
        crated_at(datetime): Дата создания/изменения
        
    Meta:
        verbose_name(str): Название модели в единственном числе
        verbose_name_plural(str): Название модели во множественном числе
    """
    
    text = models.CharField(max_length=255, unique=True, verbose_name="цитата")
    source = models.CharField(max_length=64, verbose_name="источник")
    weight = models.PositiveIntegerField(validators=[MinValueValidator(1), MaxValueValidator(100)], default=1, 
                                         help_text="1–100: чем больше, тем выше шанс выпадения", verbose_name="вес")
    likes = models.PositiveIntegerField(default=0, verbose_name="лайки")
    dislikes = models.PositiveIntegerField(default=0, verbose_name="дизлайки")
    views = models.PositiveIntegerField(default=0, verbose_name="просмотры")
    created_at = models.DateTimeField(auto_now=True, verbose_name="дата добавления")
    
    def clean(self):
        """
        Проверка на число цитат у источника
        """
        if Quote.objects.filter(source=self.source).exclude(id=self.id).count() >= 3:
            raise ValidationError("У одного источника не может быть больше трех цитат!")
    
    class Meta:
        verbose_name = "цитата"
        verbose_name_plural = "цитаты"
    