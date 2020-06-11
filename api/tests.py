import datetime

from django.test import TestCase, Client
from django.urls import reverse
from rest_framework import status

from api.models import Author
from api.serializers import AuthorSerializer

# initialize the APIClient app
client = Client()


class GetAllAuthorsTest(TestCase):
    """ Test module for GET all puppies API """

    def setUp(self):
        Author.objects.create(
            fullName='Jane Austen', birthday=datetime.date.today())
        Author.objects.create(
            fullName='Author2', description="test author2")
        Author.objects.create(
            fullName='Author3', description="test author3")
        Author.objects.create(
            fullName='Author4', description="test author4")

    def test_get_all_authors(self):
        # get API response
        response = client.get(reverse('get_all_authors'))
        # get data from db
        authors = Author.objects.all()
        serializer = AuthorSerializer(authors, many=True)
        self.assertEqual(response.data, serializer.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
