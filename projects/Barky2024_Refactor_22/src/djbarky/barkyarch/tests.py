from django.test import TestCase
from django.urls import reverse

from barkyapi.models import Bookmark
from barkyarch.domain.model import Bookmark
from barkyarch.adapters import repository


class RepositoryTests(TestCase):
    def setUp(self):
        self.repository = repository.DjangoRepository()
        self.bookmark = Bookmark(
            id=1,
            title="Awesome Django",
            url="https://awesomedjango.org/",
            notes="Best place on the web for Django.",
        )

        # print(f"bookmark id: {self.bookmark.id}")

    def test_repository_add(self):
        self.repository.add(self.bookmark)
        self.assertEqual(Bookmark.objects.count(), 1)