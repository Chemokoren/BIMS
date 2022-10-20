from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets, permissions, generics, mixins
from rest_framework.response import Response

from Utils import evaluate_stock_status
from book_inventory_app.models import Author, Book, Stock
from book_inventory_app.apis.serializers import AuthorSerializer, BookSerializer, StockSerializer,StockHistorySerializer
from rest_framework.filters import SearchFilter

class AuthorViewSet(viewsets.ModelViewSet):
    """Author ViewSet for viewing and editing authors."""
    queryset = Author.objects.all()
    serializer_class = AuthorSerializer
    permission_classes = [permissions.IsAuthenticated]


class BookViewSet(viewsets.ModelViewSet):
    """Book ViewSet for viewing and editing books."""
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [permissions.IsAuthenticated]

    def create(self, request, *args, **kwargs):
        """Create Book Object"""
        book_data = request.data
        try:
            author_info = Author.objects.get(id=book_data["author"])

        except Author.DoesNotExist:
                return Response({'message': 'Author Object does not exist!'})
        try:
            check =Book.objects.filter(title=book_data["title"]) | Book.objects.filter(description=book_data["description"])
            if check.exists():
                return Response({'message': 'Book already exists!'})
            else:
                new_book = Book.objects.create(title=book_data["title"],
                                               year_of_publication=book_data["year_of_publication"],
                                               description=book_data["description"],
                                               author=author_info
                                               )
                serializer = BookSerializer(new_book)
                return Response(serializer.data)
        except KeyError:
            return Response({'message': 'Book Creation Failed!'})


class StockViewSet(mixins.CreateModelMixin,
                   mixins.ListModelMixin,
                   mixins.RetrieveModelMixin,
                   mixins.UpdateModelMixin,
                   viewsets.GenericViewSet):
    """Stock ViewSet for viewing and editing stock."""
    queryset = Stock.objects.all()
    serializer_class = StockSerializer
    permission_classes = [permissions.IsAuthenticated]

    def create(self, request, *args, **kwargs):
        """Create Stock Model"""
        try:
            stock_data = request.data
            check = Stock.objects.filter(book=stock_data["book"])
            if check.exists():
                print("update stock")
                data = check.first()
                new_quantity = float(data.quantity) + float(stock_data["quantity"])
                res_status = evaluate_stock_status(new_quantity)
                data.quantity = new_quantity
                data.status = res_status.value
                data.description = stock_data['description'] if stock_data['description'] else data.description
                data.save()

                serializer = StockSerializer(data)
                return Response(serializer.data)
            else:
                print("create new stock")
                try:
                    book_info = Book.objects.get(id=stock_data["book"])
                except Book.DoesNotExist:
                    return Response({'message': 'Book Object does not exist!'})
                res_status = evaluate_stock_status(stock_data["quantity"])
                new_stock = Stock.objects.create(quantity=stock_data["quantity"],
                                                 description=stock_data["description"],
                                                 book=book_info,
                                                 status=res_status.value)
                serializer = StockSerializer(new_stock)

                return Response(serializer.data)


        except KeyError:
            return Response({'message': 'Creation Failed!'})

    def retrieve(self, request, *args, **kwargs):
        """Get From Stock Model"""
        try:
            stock = Stock.objects.filter(id=self.kwargs.get('pk'))
            serializer = StockSerializer(stock, many=True)
            return Response(serializer.data)
        except KeyError:
            return Response({'message': 'Retrieve Failed!'})

    def update(self, request, *args, **kwargs):
        """Update Stock Model"""
        try:
            stock_object = self.get_object()

            data = request.data
            new_quantity = int(data['quantity'])
            res_status = evaluate_stock_status(new_quantity)

            stock_object.quantity = new_quantity
            stock_object.description = data['description']
            stock_object.book = Book.objects.get(id=data['book'])
            stock_object.status = res_status.value

            stock_object.save()
            serializer = StockSerializer(stock_object)
            return Response(serializer.data)

        except KeyError:
            return Response({'message': 'Update Failed!'})

    def partial_update(self, request, *args, **kwargs):
        """Patch Stock Model"""
        try:
            stock_object = self.get_object()

            data = request.data
            new_quantity = int(data['quantity'])
            res_status = evaluate_stock_status(new_quantity)

            try:
                book_instance = Book.objects.get(id=data.get("book", stock_object.book))
            except Book.DoesNotExist:
                return Response({'message': 'Book Object does not exist!'})
            stock_object.quantity = new_quantity if new_quantity >=0 else stock_object.quantity
            stock_object.description = data['description'] if data['description'] else stock_object.description

            stock_object.book = book_instance
            stock_object.status = res_status.value if res_status else stock_object.status

            stock_object.save()
            serializer = StockSerializer(stock_object)
            return Response(serializer.data)

        except KeyError:
            return Response({'message': 'Patch Failed!'})

class StockHistoryViewSet(mixins.RetrieveModelMixin,mixins.ListModelMixin,viewsets.GenericViewSet):
    """Stock History ViewSet for viewing stock history."""
    queryset = Stock.history.all()
    serializer_class = StockHistorySerializer
    permission_classes = [permissions.IsAuthenticated]

    def retrieve(self, request, *args, **kwargs):
        """Get From StockHistory Model"""
        try:
            stock = Stock.history.filter(id=self.kwargs.get('pk'))
            serializer = StockHistorySerializer(stock, many=True)
            return Response(serializer.data)
        except KeyError:
            return Response({'message': 'Retrieve Failed!'})



class BookListFilter(generics.ListAPIView):
    """Filter Books by  year_of_publication, & author"""
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    filter_backends = (DjangoFilterBackend, SearchFilter)
    search_fields = ['year_of_publication', 'author__first_name', 'author__last_name']
