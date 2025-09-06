from django.urls import path
from .views import QuoteRetrieveApiView, QuoteCreateApiView, QuoteDetailApiView, TopQuotesAPIView

urlpatterns = [
    path('', QuoteRetrieveApiView.as_view()),
    path('create/', QuoteCreateApiView.as_view()),
    path('<int:id>/', QuoteDetailApiView.as_view()),
    path('top/', TopQuotesAPIView.as_view()),
]
