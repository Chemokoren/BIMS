from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets, permissions, generics,mixins
from rest_framework.response import Response

from Utils import evaluate_stock_status
from book_inventory_app.models import Author, Book,Stock
from book_inventory_app.apis.serializers import AuthorSerializer, BookSerializer,StockSerializer
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
        book_data = request.data

        new_book = Book.objects.create(title=book_data["title"],
                                          year_of_publication=book_data["year_of_publication"],
                                      description=book_data["description"],
                                      author=Author.objects.get(id=book_data["author"])
                                          )

        serializer = BookSerializer(new_book)

        return Response(serializer.data)

    def retrieve(self, request, *args, **kwargs):
        params = kwargs

        year_of_publication = Book.objects.filter(year_of_publication=params['pk'])
        author = Book.objects.filter(author=params['pk'])

        if year_of_publication:
            serializer = BookSerializer(year_of_publication, many=True)
            return Response(serializer.data)
        elif author:
            serializer = BookSerializer(author, many=True)
            return Response(serializer.data)

    # def update(self, request, *args, **kwargs):
    #     car_object = self.get_object()
    #     data = request.data
    #
    #     car_plan = CarPlan.objects.get(plan_name=data["plan_name"])
    #
    #     car_object.car_plan = car_plan
    #     car_object.car_brand = data["car_brand"]
    #     car_object.car_model = data["car_model"]
    #     car_object.production_year = data["production_year"]
    #     car_object.car_body = data["car_body"]
    #     car_object.engine_type = data["engine_type"]
    #
    #     car_object.save()
    #
    #     serializer = CarSpecsSerializer(car_object)
    #
    #     return Response(serializer.data)
    #
    # def partial_update(self, request, *args, **kwargs):
    #     car_object = self.get_object()
    #     data = request.data
    #
    #     try:
    #         car_plan = CarPlan.objects.get(plan_name=data["plan_name"])
    #         car_object.car_plan = car_plan
    #     except KeyError:
    #         pass
    #
    #     car_object.car_brand = data.get("car_brand", car_object.car_brand)
    #     car_object.car_model = data.get("car_model", car_object.car_model)
    #     car_object.production_year = data.get("production_year", car_object.production_year)
    #     car_object.car_body = data.get("car_body", car_object.car_body)
    #     car_object.engine_type = data.get("engine_type", car_object.engine_type)
    #
    #     car_object.save()
    #
    #     serializer = CarSpecsSerializer(car_object)
    #
    #     return Response(serializer.data)


class StockViewSet(mixins.CreateModelMixin,
                   mixins.RetrieveModelMixin,
                   mixins.UpdateModelMixin,
                   viewsets.GenericViewSet):
    """Stock ViewSet for viewing and editing stock."""
    queryset = Stock.objects.all()
    serializer_class = StockSerializer
    permission_classes = [permissions.IsAuthenticated]

    def create(self, request, *args, **kwargs):
        stock_data = request.data

        check = Stock.objects.filter(description=stock_data["description"],quantity=stock_data["quantity"],book=stock_data["book"])
        if check.exists():
            print("update stock")
            data =check.first()
            new_quantity =int(data.quantity) + int(stock_data["quantity"])
            res_status =evaluate_stock_status(new_quantity)
            data.quantity   = new_quantity
            data.status     = res_status.value
            data.save()

            serializer = StockSerializer(data)
            return Response(serializer.data)
        else:
            print("create new stock")
            res_status = evaluate_stock_status(stock_data["quantity"])
            new_stock = Stock.objects.create(quantity=stock_data["quantity"],
                                        description=stock_data["description"],
                                        book=Book.objects.get(id=stock_data["book"]),
                                        status=res_status)
            # new_stock.save()
            serializer = StockSerializer(new_stock)
            return Response(serializer.data)


    def retrieve(self, request, *args, **kwargs):
        stock = Stock.objects.filter(id=self.kwargs.get('pk'))
        serializer = StockSerializer(stock, many=True)
        return Response(serializer.data)




class BookListFilter(generics.ListAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    filter_backends = (DjangoFilterBackend,SearchFilter)
    search_fields = ['year_of_publication', 'author__first_name','author__last_name']