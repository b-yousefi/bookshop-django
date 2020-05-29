from django.conf.urls import include
from django.urls import path
from rest_framework import routers

from .views import AuthorViewSet, AddressViewSet, BookViewSet, PublicationViewSet, CategoryViewSet, OrderViewSet, \
    OrderItemViewSet, ClientViewSet, UserViewSet

router = routers.DefaultRouter()
router.register('clients', ClientViewSet)
router.register('users', UserViewSet)
router.register('authors', AuthorViewSet)
router.register('addresses', AddressViewSet)
router.register('books', BookViewSet)
router.register('publications', PublicationViewSet)
router.register('categories', CategoryViewSet)
router.register('orders', OrderViewSet)
router.register('order_items', OrderItemViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
