.. rest-api:

*******************
REST API Guidelines
*******************

The guidelines for our **REST API** are intended to make our interface more stable and to keep the implementation as consistent as possible.
Both formal and structural definitions are designed. This ``SHOULD`` also help to keep the source code uniformly easier to read.
All guidelines mentioned here ``SHOULD`` be followed if technically or conceptually possible. Individual variations ``MAY`` be possible,
but ``MUST`` then be described in the documentation.

Instruction
===========

**REST** stands for *Representational State Transfer*, **API** for *Application Programming Interface*.
This refers to a programming interface that is oriented towards the paradigms and behaviour of the World Wide Web (WWW)
and describes an approach for communication between client and server in networks.

Roy Fielding developed the concept and published it in his dissertation
`Architectural Styles and the Design of Network-based Software Architectures <https://www.ics.uci.edu/~fielding/pubs/dissertation/top.htm>`_ in 2000.

.. contents::

Principles
----------
The REST concept is based on 6 basic principles:

:Client server:
    The general requirement is that all properties of the client-server architecture apply.
:Statelessness:
    Each reply ``MUST`` contains all the information necessary for the server or client to understand the message.
:Cacheability:
    Caching ``SHOULD`` be used.
:Layered system:
    The systems are to have a multi-layer structure. This means it is sufficient to offer the user only one interface.
    The underlying layers can remain hidden, thus simplifying the overall architecture.
:Code on demand:
    This requirement is ``OPTIONAL``. Code on demand means that code can be submitted to the client code for local execution.
:Uniform interface:
    The individual interfaces ``SHOULD`` be kept as uniform as possible.

Conventions
-----------
The ``CAPITALIZED`` words throughout these guidelines have a special meaning.
The requirement level keywords:

    "MUST", "MUST NOT", "REQUIRED", "SHALL", "SHALL NOT", "SHOULD", "SHOULD NOT", "RECOMMENDED", "MAY", and "OPTIONAL"

used in this document are to be interpreted as described in `RFC 2119 <https://tools.ietf.org/html/rfc2119>`_.

General
=======
The following guidelines apply not only to the REST API itself, but also to all connections provided by DATAGERRY.

Some general principles.
    - API ``SHOULD`` be as small as possible but no smaller
    - Implementation ``SHOULD`` not impact the API

Version Control System
----------------------
Every API design ``SHOULD`` be stored in a Version Control System.
This also ``MUST`` applies to plug-in integrations or additional interfaces that are offered via our REST API.
Where possible the API design ``SHOULD`` stored in the same repository as the API implementation.

.. _naming:
Naming Conventions
------------------

1. Every identifier ``MUST`` be in english and written in lowercase.
2. An identifier ``SHOULD NOT`` contain acronyms.
3. `Kebab case` (kebab-case) ``MUST`` be used to delimit combined words.

Security
--------
Every route ``MUST`` be secured. For authentication, a valid `JSON Web token <https://tools.ietf.org/html/rfc7519>`_ ``REQUIRED`` be sent in the `HTTP Authorization` as a bearer token.

Resources
=========
REST is based on the abstraction of individual areas or components to so-called resources.
These can differ significantly from each other in their structure. In principle, a differentiation is
made between an explicit resource, a collection of resources or a special function (controller) that is to be executed.
The latter ``SHOULD`` only be implemented independently in individual cases.

Naming
------
Nouns ``MUST`` be used to identify resources. Active definitions, as well as the use of verbs ``SHOULD`` be avoided if possible,
and they ``MAY`` better result from the logical application of existing resources.
You ``MUST`` use the plural version of a resource name to be consistent when referring to particular resources.


URL
---
Every URL ``MUST`` follow the general guideline of :ref:`naming`.
Besides, a URL ``MUST NOT`` end with a trailing slash (/).

Parameters
----------

Filtering
---------

Sorting
-------

Pagination
----------

Responses
=========



TL;DR
=====

1. You ``SHOULD`` build the API with other developers in mind or better as a product itself.

- Not for a specific UI/Frontend.
- Embrace flexibility of each endpoint

2. Use collections

- ``SHOULD NOT`` have more then two endpoints per resource.
    - The resource collection (e.g. /objects)
    - Individual resource within the collection (e.g. /objects/{publicID})

- ``MUST`` use plural forms (‘objects’ instead of ‘object’)
- ``SHOULD`` keep URLs as short as possible.

3. ``MUST`` use nouns as resource names

4. ``SHOULD`` make resource representations meaningful.

- No plain IDs embedded in responses. Responses ``MUST`` have useful data.
- ``SHOULD`` design resource representations. Don’t simply represent database tables.
- ``SHOULD`` merge representations.

5. ``MUST`` support filtering, sorting, and pagination on collections.

6. ``MAY`` support field projections on resources. Allow clients to reduce the number of fields that come back in the response.

7. ``MAY`` support a caching system.

8. ``MUST`` use the HTTP method names to mean something.

    :POST:
        Create and other non-idempotent operations.

    :PUT/PATCH:
        Update or replace data.

    :GET:
        Read a resource or collection.

    :DELETE:
        Remove/delete a resource or collection.

    :``OPTIONAL`` HEAD:
        For meta information. Normally only the `GET` without a body.

9. ``MUST`` use HTTP status codes.

- The intended purpose often results from the name alone.

10. ``MUST`` Secure the API Routes

- Check if your routes have authentication.
- Check if your routes are reachable for a user.

11. ``RECOMMENDED`` to use Content-Type negotiation to describe incoming request payloads.

12. ``MUST`` versioning in the Accept header.

13. You ``SHOULD`` be ensure that your operations can be idempotent.
