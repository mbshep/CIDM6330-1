# useful guide: https://www.pythontutorial.net/python-unit-testing/python-unittest/
# note that Django's TestCase class is a subclass of Python's unittest.TestCase class so tutorials
# on unittest.TestCase are applicable to Django's TestCase class.

import unittest

from barky.domain.model import Bookmark
from barky.adapters import repository
from barky.services.uow import DjangoUnitOfWork, DjangoApiUnitOfWork


class TestCaseRepository(unittest.TestCase):
    def setUp(self) -> None:
        self.bookmark = Bookmark(
            id=1,
            title="Test Title",
            url="http://test.com",
            notes="Test notes",
            date_added="2021-01-01",
        )

    def test_repository_list(self):
        pass

    def test_repository_create(self):
        pass

    def test_repository_update(self):
        pass

    def test_repository_delete(self):
        pass

    def test_repository_get(self):
        pass
