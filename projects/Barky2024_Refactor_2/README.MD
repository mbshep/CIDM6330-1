# Barky Refactor 2
The major difference in this refactor is the inclusion of a few key concepts which are explored in depth in P&G:
- **Repository**: by abstracting state change operations on the entities within the domain, we can replace/insert any number of data persistence strategies.
    - P&G Readings: Chapters 2-5
- **Unit of Work**: The unit of work is a means of encapsulating and describing transation-like operations with your system such that any number of needed operations can be coordinated and completed that, collectively constitude an whole operation's completion.  In effect, this is more-or-less the equivalent of a database transaction.
    - P&G Readings: Chapters 6 and 7.
- Project structure with setuptools
- Use of `unittest` rather than `pytest`.

## New to Refactor 2
- Considers the Project Stucture Template from P&G from [Appendix B](https://www.cosmicpython.com/book/appendix_project_structure.html)
    - Key items here are the use of Python's [setuptools](https://setuptools.pypa.io/en/latest/setuptools.html) to make the entire application installable.  This makes references within the application easier
- Considers the [Appendix D](https://www.cosmicpython.com/book/appendix_django.html) application structure from P&G.
    - this utilizes the app structure form Appendix B to have `barky` (allocation for P&G) live alongside the Django app
    - it is not 100% certain that we'd completely live with this architecture - we might just collapase back into Django's folder/project strcuture.
- **NOTE**: we are NOT using Docker despite P&G using it (and many other Django and Python books/tutorials).  Docker is just an extra layer that I chose not to deal with as our virtual environment will be sufficient.
- **CAUTION**: the django parts are NOT launched automatially and need to be manually launched in thie refactor.  So you make sure you use one terminal to launch the django app so that another can be used to run tests in `barky`
- With this refactor's architecture, we could use the Django project directly OR the barky infrastructure as barky has been refactored to be available for other implementation strategies beyond just Django.
    - P&G presume the use of [pytest](https://docs.pytest.org/en/8.0.x/), but we'll stick to the built-in [unittest](https://docs.python.org/3/library/unittest.html) that comes with Python to remain consistent with Django.  So, new tests will be included to only test 'barky' rather than Django.  Thus, the Django parts will continue self-contain its tests.

## Barky Refactoring Roadmap
Dane Hillard's code focused on a command-line interface, but we will systematically refactor that code, across a series of branches, to do the following:

1. Replace the custom data handling (the DatabaseManager module) with the [Django O/RM](https://docs.djangoproject.com/en/5.0/topics/db/queries/)
    1. Replace the existing DatabaseManager with the Django ORM.
    2. Replace the CLI web-based REST API using the Django REST Framework.
    3. SOLID
    4. Use [DRF's testing facilities](https://www.django-rest-framework.org/api-guide/testing/#api-test-cases)
2. Adopt the suggestions from Percival and Gregory regarding the Unit of Work and Respository Pattern and Django: [Appendix D: Repository and Unit of Work Patterns with Django](https://www.cosmicpython.com/book/appendix_django.html)
    1. Add a separate Domain Model and explore the pros and cons of this: [Appendix D: Repository and Unit of Work Patterns with Django](https://www.cosmicpython.com/book/appendix_django.html)
3. Introduce messaging using Celery with Django.  This will serve as a message bus to augment event-driven architecture.
    1. [Django is well supported using Celery](https://docs.celeryq.dev/en/stable/django/first-steps-with-django.html) as an asynchronous message/task queue.
    2. Reintroduce the [Command pattern](https://refactoring.guru/design-patterns/command) as a means to encapsule the transactional intent of messages passed within Celery.
4. Improve architecture:
    1. [CQRS in general](https://douwevandermeij.medium.com/the-repository-pattern-via-cqrs-with-python-django-elasticsearch-cb38437721d3) and in [Django](https://django-cqrs.readthedocs.io/en/latest/)
    2. Dependency injection - [A good overview](https://thinhdanggroup.github.io/python-dependency-injection/), [DI with specific Flask and Django examples](https://snyk.io/blog/dependency-injection-python/), and a [Comprehensive Python Dependency Injection Framework](https://python-dependency-injector.ets-labs.org/)


## Refactor to Assignments Map
1. Refactor 1 (DRF and ORM): Assignment 5 
2. Refactor 2 (Repository Pattern and UoW ): Assignment 6
3. Refactor 3 (Celery/Messages and the Return of the Command): Assignment 7
4. Refactor 4 (CQRS and DI/Bootstrapping): Assignment 8

## Refactoring Notes relative to APP
1. The [Command](https://refactoring.guru/design-patterns/command) pattern and Barky: Whereas Barky uses the `Command` design pattern, the Django Rest Framework's [ViewSet](https://www.django-rest-framework.org/api-guide/viewsets/) structure as a controller in the [Model View Controller](https://www.askpython.com/django/django-mvt-architecture) sense.  As such, the objective of the Command pattern - to achieve a separation of concerns such that all pathways to effect a state change in the application use the same facility - is achieved with the ViewSet acting as a controller.  A Django app's views module works with DRF's ViewSet to handle the same thing.  As such, we no longer require the Command module from Barky.
