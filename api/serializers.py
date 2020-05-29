from django.contrib.auth.models import User, Group
from rest_framework import serializers
from rest_framework.authtoken.models import Token

from .models import Author, Book, Publication, Category, Order, OrderItem, Address, Client


class AddressSerializer(serializers.ModelSerializer):
    class Meta:
        model = Address
        fields = ('id', 'user', 'street', 'state', 'city', 'zipCode')


class ClientSerializer(serializers.ModelSerializer):
    class Meta:
        model = Client
        fields = ('id', 'fullName', 'phoneNumber', 'picture')


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username', 'password')
        extra_kwargs = {'password': {'write_only': True, 'required': True}}

    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)
        my_group = Group.objects.get(name='Users')
        my_group.user_set.add(user)
        user.save()
        Token.objects.create(user=user)
        return user


class BookSerializer(serializers.ModelSerializer):
    class Meta:
        model = Book
        fields = ('id', 'name', 'publishedDay', 'authors', 'publication', 'ISBN', 'summary', 'categories')


class BookMiniSerializer(serializers.ModelSerializer):
    class Meta:
        model = Book
        fields = ['id', 'name']


class AuthorSerializer(serializers.ModelSerializer):
    books = BookMiniSerializer(many=True)

    class Meta:
        model = Author
        fields = ('id', 'fullName', 'birthday', 'description', 'picture', 'books', 'no_of_books')


class PublicationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Publication
        fields = ('id', 'name', 'description', 'website')


class CategoryMiniSerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'name']


class CategorySerializer(serializers.ModelSerializer):
    children = CategoryMiniSerializer(many=True)

    class Meta:
        model = Category
        fields = ('id', 'name', 'description', 'children')


class OrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = ('id', 'user', 'address')


class OrderItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderItem
        fields = ('id', 'order', 'book', 'quantity')
