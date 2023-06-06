from rest_framework import serializers
from orders.models import Category

class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ["__all__"]
