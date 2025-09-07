from rest_framework.generics import(
    CreateAPIView,
    ListAPIView,
    RetrieveUpdateDestroyAPIView,
    RetrieveAPIView,
)
import random
from .models import Quote
from .serializers import QuoteSerializer, QuoteActionSerializer
from rest_framework.response import Response
from rest_framework import status
from django.db.models import F
from .filters import QuoteFilter
from django_filters.rest_framework import DjangoFilterBackend


class QuoteRetrieveApiView(RetrieveAPIView):
    """
    Представление для просмотра рандомной цитаты
    GET - возвращает случайную цитату и увеличивает views
    POST - увеличивает лайк или дизлайк у выбранной цитаты
    """
    
    serializer_class = QuoteSerializer
    queryset = Quote.objects.all()
    
    def get_serializer_class(self):
        if self.request.method == 'POST':
            return QuoteActionSerializer
        return QuoteSerializer
    
    def get_object(self) -> Quote:
        quote_id = self.request.session.get("current_quote_id")

        if quote_id:
            try:
                return Quote.objects.get(id=quote_id)
            except Quote.DoesNotExist:
                return None
        
        ids_weights = list(Quote.objects.values_list("id", "weight"))
        if not ids_weights:
            return None
        
        ids, weights = zip(*ids_weights)
        chosen_id = random.choices(ids, weights=weights, k=1)[0]
        quote = Quote.objects.get(id=chosen_id)
        Quote.objects.filter(id=quote.id).update(views=F("views") + 1)
        quote.refresh_from_db(fields=["views"])
        self.request.session["current_quote_id"] = quote.id
        return quote
    
    def get(self, request, *args, **kwargs):
        if self.request.method == 'GET':
            if "current_quote_id" in self.request.session:  
                del self.request.session["current_quote_id"]
        else:
            self.request.method = 'GET'
        instance = self.get_object()
        if not instance:
            return Response({"detail": "Цитат пока нет"}, status=status.HTTP_404_NOT_FOUND)
        return Response(self.get_serializer(instance).data)
        
    def post(self, request, *args, **kwargs):
        """
        Поставить like/dislike на цитату
        Ожидает {"action": "like"} или {"action": "dislike"}
        """
        instance = self.get_object()
        if not instance:
            return Response({"detail": "Цитат пока нет"}, status=status.HTTP_404_NOT_FOUND)
         
        action_serializer = QuoteActionSerializer(data=request.data)
        action_serializer.is_valid(raise_exception=True)
        action = action_serializer.validated_data["action"]

        if not id or action not in ["like", "dislike"]:
            return Response({"detail": "Неверные данные"}, status=status.HTTP_400_BAD_REQUEST)

        try:
            quote = Quote.objects.get(id=instance.id)
        except Quote.DoesNotExist:
            return Response({"detail": "Цитата не найдена"}, status=status.HTTP_404_NOT_FOUND)

        if action == "like":
            Quote.objects.filter(id=instance.id).update(likes=F("likes") + 1)
        elif action == "dislike":
            Quote.objects.filter(id=instance.id).update(dislikes=F("dislikes") + 1)

        quote.refresh_from_db(fields=["likes", "dislikes"])
        # serializer = QuoteSerializer(quote)
        # self.request.session["current_quote_id"] = quote.id
        return self.get(request, *args, **kwargs)


class QuoteDetailApiView(RetrieveUpdateDestroyAPIView):
    """
    Представление для считывания, изменения и удаления цитат
    """
    
    serializer_class = QuoteSerializer
    queryset = Quote.objects.all()
    lookup_field = "id"

class QuoteCreateApiView(CreateAPIView):
    """
    Представление для создания цитат
    """
    
    serializer_class = QuoteSerializer
    
class TopQuotesAPIView(ListAPIView):
    """
    Представление для просмотра топа цитат
    """
    
    serializer_class = QuoteSerializer
    queryset = Quote.objects.all()
    filterset_class = QuoteFilter
    filter_backends = [DjangoFilterBackend]
    