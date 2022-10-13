from rest_framework import serializers, fields

from book_inventory_app.models import Author, Book,Stock

class AuthorSerializer(serializers.ModelSerializer):
    books = serializers.StringRelatedField(many=True,read_only=True)
    class Meta:
        model  = Author
        fields = "__all__"

class BookSerializer(serializers.ModelSerializer):
    stocks =serializers.StringRelatedField(many=True,read_only=True)
    url = fields.URLField(source='get_absolute_url', read_only=True)

    class Meta:
        model  = Book
        fields = "__all__"
        depth = 1

class StockSerializer(serializers.ModelSerializer):

    class Meta:
        model  = Stock
        fields = "__all__"
