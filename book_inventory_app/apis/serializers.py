from rest_framework import serializers, fields

from book_inventory_app.models import Author, Book,Stock

class AuthorSerializer(serializers.ModelSerializer):
    """Author Serializer"""
    books = serializers.StringRelatedField(many=True,read_only=True)
    class Meta:
        model  = Author
        fields = "__all__"

class BookSerializer(serializers.ModelSerializer):
    """Book Serializer"""
    stocks =serializers.StringRelatedField(many=True,read_only=True)
    url = fields.URLField(source='get_absolute_url', read_only=True)

    class Meta:
        model  = Book
        fields = "__all__"
        depth = 1

class StockSerializer(serializers.ModelSerializer):
    """Stock Serializer"""
    class Meta:
        model  = Stock
        fields = "__all__"

class StockHistorySerializer(serializers.ModelSerializer):
    """StockHistory Serializer"""
    class Meta:
        model = Stock.history.model
        fields = "__all__"
