from django.contrib.auth.models import User
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.permissions import IsAdminUser, AllowAny
from rest_framework.response import Response

from .models import Author, Address, Book, Publication, Category, Order, OrderItem, Client
from .permissions import IsStaffOrTargetUser, IsStaffOrTargetUserObject, \
    IsStaffOrTargetOrderObject
from .serializers import AuthorSerializer, AddressSerializer, BookSerializer, PublicationSerializer, CategorySerializer, \
    OrderSerializer, OrderItemSerializer, UserSerializer


class ClientViewSet(viewsets.ModelViewSet):
    queryset = Client.objects.all()
    serializer_class = UserSerializer

    def get_permissions(self):
        if self.request.method == 'DELETE':
            return [IsAdminUser()]
        elif self.request.method == 'POST':
            return [AllowAny()]
        else:
            return [IsStaffOrTargetUser()]


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer

    def get_permissions(self):
        if self.request.method == 'DELETE':
            return [IsAdminUser()]
        elif self.request.method == 'POST':
            return [AllowAny()]
        else:
            return [IsStaffOrTargetUser()]


class AuthorViewSet(viewsets.ModelViewSet):
    queryset = Author.objects.all()
    serializer_class = AuthorSerializer

    @action(detail=True, methods=['POST'])
    def add_book(self, request, pk=None):
        if 'bookName' in request.data:
            author = Author.objects.get(id=pk)
            bookName = request.data['bookName']
            user = request.user
            print(user)
            print('author name', author.fullName)
            try:
                book = Book.objects.get(author=author.id)
                book.name = bookName
                book.save()
                serializer = BookSerializer(book, many=False)
                response = {'message': 'book updated', 'result': serializer.data}
                return Response(response, status=status.HTTP_200_OK)
            except:
                book = Book.objects.create(author=author, name=bookName)
                serializer = BookSerializer(book, many=False)
                response = {'message': 'book created', 'result': serializer.data}
                return Response(response, status=status.HTTP_200_OK)

        else:
            response = {'message': 'you need to pass stars'}
            return Response(response, status=status.HTTP_400_BAD_REQUEST)

    def update(self, request, *args, **kwargs):
        response = {'message': 'Only admin can perform update'}
        return Response(response, status=status.HTTP_403_FORBIDDEN)


class PublicationViewSet(viewsets.ModelViewSet):
    queryset = Publication.objects.all()
    serializer_class = PublicationSerializer


class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer


class BookViewSet(viewsets.ModelViewSet):
    queryset = Book.objects.all()
    serializer_class = BookSerializer


class AddressViewSet(viewsets.ModelViewSet):
    queryset = Address.objects.all()
    serializer_class = AddressSerializer

    @action(detail=False, methods=['POST'])
    def add_address(self, request, pk=None):
        user = request.user
        address = Address.objects.create(user=user, city=request.date['city'], state=request.date['state']
                                         , street=request.date['street'])
        serializer = AddressSerializer(address, many=False)
        response = {'message': 'address created', 'result': serializer.data}
        return Response(response, status=status.HTTP_200_OK)

    def get_permissions(self):
        return [IsStaffOrTargetUserObject()]


class OrderViewSet(viewsets.ModelViewSet):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    permission_classes = (IsStaffOrTargetUserObject,)


class OrderItemViewSet(viewsets.ModelViewSet):
    queryset = OrderItem.objects.all()
    serializer_class = OrderItemSerializer
    permission_classes = (IsStaffOrTargetOrderObject,)
