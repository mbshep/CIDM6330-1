from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIRequestFactory, APITestCase

from .models import Bookmark

# Create your tests here.
# test plan
# 1. create a bookmark
class BookmarkTests(APITestCase):
    def test_create_bookmark(self):
        """
        Ensure we can create a new bookmark object.
        """
        url = reverse("bookmarks")
        data = {"title": "Django REST framework", "url": "https://www.django-rest-framework.org/"}
        response = self.client.post(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Bookmark.objects.count(), 1)
        self.assertEqual(Bookmark.objects.get().title, "Django REST framework") 

# 2. retrieve a bookmark
# 3. delete a bookmark
# 4. list bookmarks
# 5. update a bookmark
# 6. create a snippet
# 7. retrieve a snippet
# 8. delete a snippet
# 9. list snippets
# 10. update a snippet
# 11. create a user
# 12. retrieve a user
# 13. delete a user
# 14. list users
# 15. update a user
# 16. highlight a snippet
# 17. list bookmarks by user
# 18. list snippets by user
# 20. list bookmarks by date
# 21. list snippets by date
# 23. list bookmarks by title
# 24. list snippets by title
# 26. list bookmarks by url
# 27. list snippets by url

