from rest_framework.generics import(
    CreateAPIView,
    ListAPIView,
    RetrieveUpdateDestroyAPIView,
    RetrieveAPIView,
)
import random
from .models import Quote
from .serializers import QuoteSerializer
from django.db.models import F


class QuoteRetrieveApiView(RetrieveAPIView):
    """
    Представление для просмотра рандомной цитаты
    """
    
    serializer_class = QuoteSerializer
    queryset = Quote.objects.all()
    
    def get_object(self) -> Quote:
        ids_weights = list(Quote.objects.values_list("id", "weight"))
        if not ids_weights:
            quote = None
        else:
            ids, weights = zip(*ids_weights)
            chosen_id = random.choices(ids, weights=weights, k=1)[0]
            quote = Quote.objects.get(id=chosen_id)
            Quote.objects.filter(id=quote.id).update(views=F("views") + 1)
            quote.refresh_from_db(fields=["views"])
        return quote

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

    def get_queryset(self):
        filter_type = self.request.query_params.get("filter", "popular")
        
        qs = Quote.objects.all()

        if filter_type == "popular":
            qs = qs.order_by("-likes", "-views", "-created_at")[:10]
            
        elif filter_type == "unpopular":
            qs = qs.order_by("-dislikes", "-views", "-created_at")[:10]
            
        elif filter_type == "new":
            qs = qs.order_by("-created_at")[:10]
            
        else:
            qs = qs.order_by("-likes", "-views", "-created_at")[:10]

        return qs
    