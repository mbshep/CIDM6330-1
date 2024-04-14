from __future__ import annotations
import abc
from django.db import transaction
from barkyarch.adapters import repository


class AbstractUnitOfWork(abc.ABC):
    bookmarks: repository.AbstractRepository

    # __enter__ and __exit__ methods are used to create a context manager
    # https://www.pythonmorsels.com/every-dunder-method/#context-managers
    def __enter__(self) -> AbstractUnitOfWork:
        return self

    def __exit__(self, *args):
        self.rollback()

    @abc.abstractmethod
    def commit(self):
        raise NotImplementedError

    @abc.abstractmethod
    def rollback(self):
        raise NotImplementedError


class DjangoUnitOfWork(AbstractUnitOfWork):
    def __enter__(self):
        self.bookmarks = repository.DjangoRepository()
        # Django ORM has its own transaction management system - https://docs.djangoproject.com/en/5.0/topics/db/transactions/
        # tell Django to stop automatically committing each ORM operation immediately
        # so that we can to what we want. Honestly, we are fighting against Django's ORM here.
        transaction.set_autocommit(False)
        return super().__enter__()

    def __exit__(self, *args):
        super().__exit__(*args)
        transaction.set_autocommit(True)

    def commit(self):
        # explicit rollback and commits are not normally needed in the Django ORM
        # however, we must manually update each object that has been modified
        for bm in self.bookmarks.bookmarks_set:
            self.bookmarks.bookmarks_set.update(bm)
        transaction.commit()

    def rollback(self):
        # explicit rollback and commits are not normally needed in the Django ORM
        transaction.rollback()


class DjangoApiUnitOfWork(AbstractUnitOfWork):
    def __enter__(self):
        # self.batches = repository.DjangoRepository()
        # transaction.set_autocommit(False)
        # return super().__enter__()
        pass

    def __exit__(self, *args):
        # super().__exit__(*args)
        # transaction.set_autocommit(True)
        pass

    def commit(self):
        # for batch in self.batches.seen:
        #     self.batches.update(batch)
        # transaction.commit()
        pass

    def rollback(self):
        # transaction.rollback()
        pass
