# Barky Refactor 22
The major difference in this refactor is the inclusion of a few key concepts which are explored in depth in P&G:
- **Repository**: by abstracting state change operations on the entities within the domain, we can replace/insert any number of data persistence strategies.
    - P&G Readings: Chapters 2-5
- **Unit of Work**: The unit of work is a means of encapsulating and describing transation-like operations with your system such that any number of needed operations can be coordinated and completed that, collectively constitude an whole operation's completion.  In effect, this is more-or-less the equivalent of a database transaction.
    - P&G Readings: Chapters 6 and 7.
- Project structure with setuptools
- Use of `unittest` rather than `pytest`.

## Why is there a Refactor 22?
Django is a monolithic architecture whose bootstrap process expects the settings.py module to be read from within the root/base project where all additional apps are listed.  Any given app can use other **utility** code, but Django doesn't want other code to call its elements without considerable additional effort to **ignite** Django's own bootstrap process first.

Thus, regardless of whether we place our archiecture completely outside of the Django project (ensuring that PYTHONPATH is set to include that location), or even within the Django project structure, Django expects its own setup routine to be first called, with settings set, before any Django things can happen. This is normal behavior for a [monolithic architecture](https://www.linkedin.com/pulse/understanding-architecture-django-monolithic-approach-amin-zamani/).  Whereas in their last chapters, P&G introduce a bootstrap, we do not need a bootstrap as Django handles that.

So, there are probably a few things we'll need to re-examine:
- **Repository** - we can still do this, but it must be tested via one of the Apps you've identified in Django's settings.  Whereas I'm sure we can use the repository now to bypass Django's O/RM, it seems mostly wierd to make our respository an app within Django


## New to Refactor 22
In this refactor, we have three main choices to consider if we wan't any Django-adjacent things like the services, domain, and adapters from P&G (Django views are considered endpoints).  Don't forget that [Django's MVT](https://www.geeksforgeeks.org/django-project-mvt-structure/) is itself an architectural pattern.

1. *Option 1* is to leave architecture code outside of Django folder/file structure and considering using setuptools to make it an installable package (which we left behind in refactor 2).  This is fine but the actual cross-talk will still require that testing this package happens within Django.
2. *Option 2* is the place architecture code witin Django's structure, but this does not exonerate us from needing to ensure that Django's bootstrap/setup process still launches.  We still can't test from within the module without extra hassle, so this seems like it'll be better than option 1, but that's not really the case either.
3. *Option 3* is that we make the repository and other architectural code a Django app itself and thus tightly coupling the presumably independent architecture to Django's itself.  This option makes testing and cross-communication much easier.

### A fourth way
A fourth way would be to write other code that accesses the endpoints of the DRF services we expose and leave Django to its own devices.  We can demonstrate this, but we still would be resigned to just this method as Django's O/RM can't be used outside of Django without running Django.  Testing endpoints is fine and this creates a hybrid where Django is still being used more for a micro-services arhictecture rather than the contining monolith.  We would not use any of Django's templating or presentation capabilities with this approach.

### We Won't Continue Down this Path
We will not likely put the effort into the CRUD (repository pattern) and transaction (Unit Of Work) facilities of the architectural patterns from chapters 1 to 7 with Django as features or facilities that exist **OUTSIDE** of the Django project framework.  This is because we are fundamentally fighting Django to get these done.  This is probably why P&G chose Flask/SQLAlchemy as they are more loosely coupled which makes it easier to include them as part of an overall architecture.

However, we can more readily and easily implement these within the Django project structure.  While this is indeed feasible, it lessens the impact and advantage of the pattern as we are not truly independent of Django.  There are valid workarounds, but they stray back into the territory of fighting the intrinsic design of the Django Framework.

Although potentially very easy to miss, P&G realize that they have to coerce Django to play outside of the Django project structure with their discussion in this part of Appendix D: [API: Django Views Are Adapters](https://www.cosmicpython.com/book/appendix_django.html#_api_django_views_are_adapters):

```python
os.environ["DJANGO_SETTINGS_MODULE"] = "djangoproject.django_project.settings"
django.setup()


@csrf_exempt
def add_batch(request):
    data = json.loads(request.body)
    eta = data["eta"]
    if eta is not None:
        eta = datetime.fromisoformat(eta).date()
    services.add_batch(
        data["ref"], data["sku"], data["qty"], eta,
        unit_of_work.DjangoUnitOfWork(),
    )
    return HttpResponse("OK", status=201)


@csrf_exempt
def allocate(request):
    data = json.loads(request.body)
    try:
        batchref = services.allocate(
            data["orderid"],
            data["sku"],
            data["qty"],
            unit_of_work.DjangoUnitOfWork(),
        )
    except (model.OutOfStock, services.InvalidSku) as e:
        return JsonResponse({"message": str(e)}, status=400)

    return JsonResponse({"batchref": batchref}, status=201)
```

P&G discuss the ins and outs of Django app architecture and refer to [this post](https://forum.djangoproject.com/t/where-to-put-business-logic-in-django/282/7) on the matter of how to extend/modify Django's out-of-the-box design when/as needed.  Of course, the book's [Epilogue](https://www.cosmicpython.com/book/epilogue_1_how_to_get_there_from_here.html) is also a great read on the matter of how to balance and make sense out of the book's material.

## Updated project strcuture

- **djbarky** - the main Django project
- **barkyapi** - the DRF app
- **barkyarch** - the architectural elements that mirror those from P&G

I do not anticipate leaving things this way for refactor 3 and 4 as we might simply let Django be a monolith and operate within Django to capitilize on a hybrid approach between monolithic and microservices.

### Repository Pattern and Django

There are some articles and resources that demonstrate implementing the Repository Pattern in Django (or argue against them):
- **P&G**: [Appendix D](https://www.cosmicpython.com/book/appendix_django.html) has quite a bit of valuable discussion on the the topic in addition to the sample code given.
- [Arjun Adhikari | Python is Love](https://pythonislove.com/repository-design-pattern-in-django) provides a nice walkthrough with some useful code examples.
- [Roy Manigley | Django Repository Pattern](https://github.com/roymanigley/django-repository-pattern) - this is one of the more straight-foward approaches you can use.
- [James Bennet | Against service layers in Django](https://www.b-list.org/weblog/2020/mar/16/no-service/) - the argument against bothing with service layers such as the repository and UoW patterns.  Don't forget, Django is the "monolith."  
- [Luke Plant | Django Views - The Right Way](https://spookylukey.github.io/django-views-the-right-way/index.html) In the end, any service layer is activated/engaged from views: [there are many practices to consider when it comes to handling view design](https://spookylukey.github.io/django-views-the-right-way/index.html).
- [Douwe va der Meij | The repository pattern via CQRS with Python/Django/Elasticsearch](https://douwevandermeij.medium.com/the-repository-pattern-via-cqrs-with-python-django-elasticsearch-cb38437721d3) - a full treatment that looks forward.

### Unit of Work and Django
- [sepehr akbarzadeh | Revolutionize Your Data Handling with the Unit of Work Design Pattern in Python and Django](https://python.plainenglish.io/revolutionize-your-data-handling-with-the-unit-of-work-design-pattern-in-python-and-django-14895d147cdc) - Good overview article.
- [Manuel Kanetscheider | A Python Implementation of the Unit of Work and Repository Design Pattern using SQLModel](https://dev.to/manukanne/a-python-implementation-of-the-unit-of-work-and-repository-design-pattern-using-sqlmodel-3mb5) - also a good overview.
- [Transactions in Django](https://docs.djangoproject.com/en/5.0/topics/db/transactions/) - the Unit of Work is an abstraction for transaction management, which Django does natively.

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

### Helpful Articles for this Refactor:
- [Gabriel Saldaña | How to use Django models in external Python scripts](https://blog.gabrielsaldana.org/using-django-models-in-external-python-scripts/) - Vital if we are going to leverage the Django ORM outside of Django - very [kludgey](https://en.wikipedia.org/wiki/Kludge), so not a long-term strategy.
- [Adam Green | aShould You Use Python pathlib or os?](https://betterprogramming.pub/should-you-be-using-pathlib-6f3a0fddec7e) - good for mapping between both approaches to working with path information.
- [SO | How to call django.setup() in console_script?](https://stackoverflow.com/questions/39704298/how-to-call-django-setup-in-console-script) - some useful examples of how to use some of the built-in methods.
- [Django Docs | How applications are loaded](https://docs.djangoproject.com/en/5.0/ref/applications/#how-applications-are-loaded) - working with `Django.setup()`, settings, and apps.
- The [unittest - unit testing framework](https://docs.python.org/3/library/unittest.html#) - built into Python.
- [Ivan Zakrevsky|About my experience of using Django Framework](https://emacsway.github.io/en/django-framework/) - good review of the Django experience with attention to how Django does not give us much room for the [Repository](https://emacsway.github.io/en/django-framework/#active-record) and [UoW](https://emacsway.github.io/en/django-framework/#transactional-consistency-of-data) patterns.
- [Jordi Fierro | Clean Architecture in Django](https://medium.com/21buttons-tech/clean-architecture-in-django-d326a4ab86a9) - Very good explanation of the Clean Architecture in Django - we end up writing around the framework.