from django.db import transaction
from django.test import TestCase
from django.urls import reverse
from django.utils.timezone import localtime

from barkyapi.models import Bookmark
from barkyarch.domain.model import DomainBookmark
from barkyarch.services.commands import (
    AddBookmarkCommand,
    ListBookmarksCommand,
    DeleteBookmarkCommand,
    EditBookmarkCommand,
)


class TestCommands(TestCase):
    def setUp(self):
        right_now = localtime().date()

        self.domain_bookmark_1 = DomainBookmark(
            id=1,
            title="Test Bookmark",
            url="http://www.example.com",
            notes="Test notes",
            date_added=right_now,
        )

        self.domain_bookmark_2 = DomainBookmark(
            id=2,
            title="Test Bookmark 2",
            url="http://www.example2.com",
            notes="Test notes 2",
            date_added=right_now,
        )

    def test_command_add(self):
        add_command = AddBookmarkCommand()
        add_command.execute(self.domain_bookmark_1)

        # run checks

        # one object is inserted
        self.assertEqual(Bookmark.objects.count(), 1)

        # that object is the same as the one we inserted
        self.assertEqual(Bookmark.objects.get(
            id=1).url, self.domain_bookmark_1.url)

    def test_command_delete(self):
        # make sure there is a bookmark to delete
        add_command = AddBookmarkCommand()
        add_command.execute(self.domain_bookmark_2)
        # now lets try to delete it
        delete_command = DeleteBookmarkCommand()
        delete_command.execute(self.domain_bookmark_2)

        # run checks

        # the item added has been deleted
        self.assertEqual(Bookmark.objects.count(), 0)

    def test_command_list(self):
        # get two bookmarks into the database
        add_command = AddBookmarkCommand()
        add_command.execute(self.domain_bookmark_1)
        add_command.execute(self.domain_bookmark_2)
        list_command = ListBookmarksCommand()
        list_command.execute(self.domain_bookmark_2)

        # run checks

        # two objects are inserted
        self.assertEqual(Bookmark.objects.count(), 2)


'''    def test_command_edit(self):

        right_now = localtime().date()
        # get a bookmark into the database
        add_command = AddBookmarkCommand()
        add_command.execute(self.domain_bookmark_1)

        # add in changes for bookmark_1
        self.domain_bookmark_1 = DomainBookmark(
            id=1,
            title="Updated Bookmark",
            url="http://www.example_new.com",
            notes="  New Test notes",
            date_added=right_now,
        )

        edit_command = EditBookmarkCommand()
        edit_command.execute(self.domain_bookmark_1)

        # run checks

        # one objects is inserted
        self.assertEqual(Bookmark.objects.count(), 1)

        # that object is the same as the one we updated
        self.assertEqual(Bookmark.objects.get(
            id=1).url, self.domain_bookmark_1.url)'''
