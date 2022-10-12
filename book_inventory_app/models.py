from django.db import models
import django.utils.timezone
from rest_framework.reverse import reverse
from Utils import Status

class Author(models.Model):
    """Author Model"""
    first_name      = models.CharField(max_length=50)
    last_name       = models.CharField(max_length=50)
    email           = models.EmailField(db_index=True, unique=True)
    date_of_birth   = models.DateTimeField(null=True,blank=True, default=django.utils.timezone.now)

    class Meta:
        ordering = ['-id']
    def get_absolute_url(self):
        return reverse("book_inv_apis:author-detail", args=[str(self.id)])

    def __str__(self):
        return f"Author: {self.first_name} {self.last_name}"

class Book(models.Model):
    """Book Model"""
    title               = models.CharField(max_length=50)
    year_of_publication = models.CharField(max_length=50)
    description         = models.TextField(db_index=True, unique=True)
    author              = models.ForeignKey(Author, related_name="books", on_delete=models.CASCADE)

    class Meta:
        ordering = ['-id']
    def get_absolute_url(self):
        return reverse("book_inv_apis:book-detail", args=[str(self.id)])

    def __str__(self):
        return f"Book: {self.title}"


class Stock(models.Model):
    """Stock Model"""
    STATUS_CHOICES = [
        ('Good', Status.GOOD.value),
        ('Bad', Status.BAD.value),
        ('Critical', Status.CRITICAL.value),
        ('OS', Status.OUT_OF_STOCK.value)
    ]
    book          = models.ForeignKey(Book, related_name="stocks", on_delete=models.CASCADE)
    quantity      = models.CharField(max_length=50)
    description   = models.TextField(db_index=True, unique=True)
    status        = models.CharField(max_length=23, choices=STATUS_CHOICES, null=True, blank=True, default=Status.GOOD.value)


    class Meta:
        ordering = ['-id']
    def get_absolute_url(self):
        return reverse("book_inv_apis:stock-detail", args=[str(self.id)])

    def __str__(self):
        return f"Stock: {self.description}"