# Barky Refactor 4

The final steps are to consider three things from P&G's APP:

- External message bus
- Dependency Injection
- Bootstrapping

## External Message Bus

By now, I've adopted a familiar pattern where I use any excuse to just revert to things that are friendly to the Django monolithic architecture, which is fine.  Django is stable, relatively older, and qualifies as [boring tech](https://mcfunley.com/choose-boring-technology).  It is imporant to be warying of reinventing the wheel, but to also be aware of how (and why) a monolith like Django does implement [Patterns of Enterprise Application Architecture](https://martinfowler.com/eaaCatalog/index.html).

### Django Channels

While [Django Channels](https://channels.readthedocs.io/en/latest/) is not a native project within the Django Project itself, it is highly adjacent (like the [Django Rest Framework](https://www.django-rest-framework.org/) is) and will likely remain consistent with Django for years to come.

## Dependency Injection

Neither Python nor Django have a native facility for [Dependency Injection](https://martinfowler.com/articles/injection.html), which is also often called the [Inversion of Control](https://en.wikipedia.org/wiki/Dependency_inversion_principle).

Dependency Injection is among the 5 SOLID principles, each of which we would have studied closer had the book been available to me.

However, here they are:
- [Single Responsibility Principle](https://en.wikipedia.org/wiki/Single_responsibility_principle)
- [Open-Close Princple](https://en.wikipedia.org/wiki/Open%E2%80%93closed_principle)
- [Liskov Substitution Principle](https://en.wikipedia.org/wiki/Liskov_substitution_principle)
- [Interface Segregation Principle](https://en.wikipedia.org/wiki/Interface_segregation_principle)
- [Dependcy Inversion Principle](https://en.wikipedia.org/wiki/Dependency_inversion_principle)

With DI, we are doing this:

We use the dependency inversion principle to address potential coupling issues. Looseness of coupling allows for parts of a system to evolve independently.  When two software modules depend on each other, Dependency Injection holds that we should consider relationships between higher-level modules that specify **WHAT** will happen, and lower-level modules that will specify **HOW** something will happen.  With dependency injection,  the goal is to separate higher-level modules from keeping track of (or being responsible for) the low-level module implementation details. Thus, the goals of DI are:

- High-level modules should not import anything from low-level modules and instead rely on abstractions. The Commands are designed this way in our project.
- Abstractions (higher level) should not depend on details but rather the details (lower-level) should depend on abstractions.

If both higher-level and lower-level objectsdepend on the same abstractions we invert how the depency is specified - You'll be driving a rental car, but which actual car you get is dependency that is `injected` at the time of rental car checkin.

Dependency Injection informs the design of interactions between higher-level and lower-level modules where the details of this interaction are abstracted. The lower-level module is designed purposefully to know about the **WHAT** as the **HOW** is immaterial: the expected result will be assured.

The linked Wiki article diagrams the differences thusly:

A straightforward pattern can be seen here, but one where the dependencies are all rigid:

![Traditional Approach](../../docs/img/Traditional_Layers_Pattern.png)

A Dependency Inversion approach can be seen here:

![DIP Approach](../../docs/img/DIPLayersPattern.png)

- Channels
- Signals

## The Django Signals Option

From the Django documentation:

> Django includes a “signal dispatcher” which helps decoupled applications get notified when actions occur elsewhere in the framework. In a nutshell, signals allow certain senders to notify a set of receivers that some action has taken place. They’re especially useful when many pieces of code may be interested in the same events.

This will handily accommodate the premise of the internal message bus (from P&G):

> The Message Bus Maps Events to Handlers: A message bus basically says, "When I see this event, I should invoke the following handler function." In other words, it’s a simple publish-subscribe system. Handlers are subscribed to receive events, which we publish to the bus.

Django Signals does what P&G describe and, as we have opted for the monolith, then we'll just go the Django Signals route.

Django Signals provides a relatively limited built-in vocabulary for known events, but the provided set of signals cover a majority of use cases.  The built-in signals (a signal is our event) include the following categories:
- [Model Signals](https://docs.djangoproject.com/en/5.0/ref/signals/#module-django.db.models.signals)
- [Management Signals](https://docs.djangoproject.com/en/5.0/ref/signals/#management-signals)
- [Request/Response Signals](https://docs.djangoproject.com/en/5.0/ref/signals/#module-django.core.signals)
- [Test Signals](https://docs.djangoproject.com/en/5.0/ref/signals/#module-django.test.signals)

If those built-in signals do not work for us, we can also [define any custom signal](https://docs.djangoproject.com/en/5.0/topics/signals/#defining-and-sending-signals).

## New to Refactor 3

- For simplicity, I'll be using Django Signals rather than Celery.
- As we are moving entirely into the Django monolith, remove the editable package: `pip uninstall barky`

## Barky Refactoring Roadmap

Dane Hillard's code focused on a command-line interface, but we will systematically refactor that code, across a series of branches, to do the following:

1. Replace the custom data handling (the DatabaseManager module) with the [Django O/RM](https://docs.djangoproject.com/en/5.0/topics/db/queries/)
   1. Replace the existing DatabaseManager with the Django ORM.
   1. Replace the CLI web-based REST API using the Django REST Framework.
   1. SOLID
   1. Use [DRF's testing facilities](https://www.django-rest-framework.org/api-guide/testing/#api-test-cases)
1. Adopt the suggestions from Percival and Gregory regarding the Unit of Work and Respository Pattern and Django: [Appendix D: Repository and Unit of Work Patterns with Django](https://www.cosmicpython.com/book/appendix_django.html)
   1. Add a separate Domain Model and explore the pros and cons of this: [Appendix D: Repository and Unit of Work Patterns with Django](https://www.cosmicpython.com/book/appendix_django.html)
1. Introduce messaging using Celery with Django. This will serve as a message bus to augment event-driven architecture.
   1. [Django is well supported using Celery](https://docs.celeryq.dev/en/stable/django/first-steps-with-django.html) as an asynchronous message/task queue.
   1. Reintroduce the [Command pattern](https://refactoring.guru/design-patterns/command) as a means to encapsule the transactional intent of messages passed within Celery.
1. Improve architecture:
   1. [CQRS in general](https://douwevandermeij.medium.com/the-repository-pattern-via-cqrs-with-python-django-elasticsearch-cb38437721d3) and in [Django](https://django-cqrs.readthedocs.io/en/latest/)
   1. Dependency injection - [A good overview](https://thinhdanggroup.github.io/python-dependency-injection/), [DI with specific Flask and Django examples](https://snyk.io/blog/dependency-injection-python/), and a [Comprehensive Python Dependency Injection Framework](https://python-dependency-injector.ets-labs.org/)

## Refactor to Assignments Map

1. Refactor 1 (DRF and ORM): Assignment 5
1. Refactor 2 (Repository Pattern and UoW ): Assignment 6
1. Refactor 3 (Django Signals and the Return of the Command): Assignment 7
1. Refactor 4 (Django Channels to approximate CQRS and DI/Bootstrapping): Assignment 8
