from django.contrib.auth.models import User
from django.core.validators import MinValueValidator
from django.core.validators import RegexValidator
from django.db import models


class Client(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    fullName = models.CharField(max_length=100, blank=False)
    phoneNumber = models.CharField(max_length=13, validators=[
        RegexValidator(
            regex='^\+98\d{10}$',
            message='phone number pattern is invalid',
        ),
    ])
    picture = models.ImageField(upload_to='users_pics', blank=True)


class Author(models.Model):
    fullName = models.CharField(max_length=100, blank=False, unique=True)
    birthday = models.DateField(null=True, blank=True)
    description = models.TextField(max_length=100000, null=True, blank=True)
    picture = models.ImageField(upload_to='authors_pics', blank=True)

    def no_of_books(self):
        books = Book.objects.filter(authors=self)
        return len(books)


class Publication(models.Model):
    name = models.CharField(max_length=100, blank=False)
    description = models.TextField(max_length=100000, null=True, blank=True)
    website = models.URLField(max_length=250, null=True, blank=True)


class Category(models.Model):
    name = models.CharField(max_length=50, blank=False)
    description = models.TextField(max_length=100000, null=True, blank=True)
    parentCat = models.ForeignKey('self', on_delete=models.CASCADE, null=True, blank=True
                                  , related_name='children')

    class Meta:
        unique_together = (('name', 'parentCat'),)


class Book(models.Model):
    name = models.CharField(max_length=100, blank=False)
    publishedDay = models.DateField(null=True, blank=True)
    authors = models.ManyToManyField(Author, related_name='books')
    publication = models.ForeignKey(Publication, on_delete=models.CASCADE)
    ISBN = models.CharField(max_length=15, validators=[
        RegexValidator(
            regex='^(?:ISBN(?:-1[03])?:? )?(?=[0-9X]{10}$|(?=(?:[0-9]+[- ]){3})[- 0-9X]{13}$|97[89][0-9]{10}$|(?=(?:[0-9]+[- ]){4})[- 0-9]{17}$)(?:97[89][- ]?)?[0-9]{1,5}[- ]?[0-9]+[- ]?[0-9]+[- ]?[0-9X]$',
            message='ISBN pattern is invalid',
        ),
    ])
    summary = models.TextField(max_length=100000, null=True, blank=True)
    categories = models.ManyToManyField(Category)


class Address(models.Model):
    street = models.CharField(max_length=100, blank=False)
    state = models.CharField(max_length=50, blank=False)
    city = models.CharField(max_length=50, blank=False)
    zipCode = models.CharField(max_length=10, blank=False)
    user = models.ForeignKey(Client, on_delete=models.CASCADE, related_name='addresses')


class Order(models.Model):
    user = models.ForeignKey(Client, on_delete=models.CASCADE, null=False)
    address = models.ForeignKey(Address, null=False, on_delete=models.DO_NOTHING)
    placedAt = models.DateField(auto_now_add=True)
    updatedAt = models.DateTimeField(auto_now=True)


class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    book = models.ForeignKey(Book, null=False, on_delete=models.CASCADE)
    quantity = models.IntegerField(validators=[MinValueValidator(1)], default=1)

    class Meta:
        unique_together = (('book', 'order'),)
