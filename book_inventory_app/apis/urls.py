from django.urls import path, include
from rest_framework.routers import DefaultRouter
from book_inventory_app.apis.views import AuthorViewSet, BookViewSet, StockViewSet, BookListFilter,StockHistoryViewSet

app_name = 'book_inv_apis'

router =DefaultRouter()

router.register('authors',AuthorViewSet, basename="author")
router.register('books',BookViewSet, basename="book")
router.register('stock',StockViewSet, basename="stock")
router.register('history',StockHistoryViewSet, basename="stock-history")

urlpatterns = [
    path('', include(router.urls)),
    path('books/list',BookListFilter.as_view(), name="book-search")

]