from django.test import TestCase
from django.urls import reverse
from django.utils.timezone import localtime

from barkyapi.models import Bookmark
from barkyarch.domain.model import DomainBookmark
from barkyarch.adapters import repository


class RepositoryTests(TestCase):
    def setUp(self):

        rightnow = localtime().date()

        print(f"rightnow: {rightnow}")

        self.repository = repository.DjangoRepository()
        self.domain_bookmark = DomainBookmark(
            id=1,
            title="Awesome Django",
            url="https://awesomedjango.org/",
            notes="Best place on the web for Django.",
            date_added="2024-01-01",
        )

        print(f"bookmark id: {self.domain_bookmark.id}")

    def test_repository_add(self):
        self.repository.add(self.domain_bookmark)
        self.assertEqual(Bookmark.objects.count(), 1)
