from rest_framework import serializers
from .models import Quote

class QuoteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Quote
        fields = ["id", "text", "source", "weight", "likes", "dislikes", "views", "created_at"]
        read_only_fields = ["id", "likes", "dislikes", "views", "created_at"]
    
    def validate_weight(self, value):
        if not (1 <= value <= 100):
            raise serializers.ValidationError("Вес должен быть от 1 до 100")
        return value
    
    def validate(self, data):
        source = data.get("source")
        if source:
            qt = Quote.objects.filter(source=source)
            if self.instance:
                qt = qt.exclude(id=self.instance.id)
            if qt.count() >= 3:
                raise serializers.ValidationError("У одного источника не может быть больше трех цитат!")
        return data
