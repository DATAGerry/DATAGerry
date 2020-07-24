.. rest-api:

*******************
REST API Guidelines
*******************

The guidelines for our **REST API** are intended to make our interface more stable and to keep the implementation as consistent as possible.
Both formal and structural definitions are designed. This ``SHOULD`` also help to keep the source code uniformly easier to read.
All guidelines mentioned here ``SHOULD`` be followed if technically or conceptually possible. Individual variations ``MAY`` be possible,
but ``MUST`` then be described in the documentation.

.. todo::
    Add examples for every guideline - MH

.. warning::
    This guideline has just been created and will probably be implemented by default starting with DATAGERRY version 1.3.0.
    Possible variations within the implementation are therefore possible and also probable. We will work on the individual parts one after the other.

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

Naming
------
Nouns ``MUST`` be used to identify resources. Active definitions, as well as the use of verbs ``SHOULD`` be avoided if possible,
and they ``MAY`` better result from the logical application of existing resources.
You ``MUST`` use the plural version of a resource name to be consistent when referring to particular resources.
The basic rule for defining resources ``SHOULD`` be to create only those resources that are absolutely necessary.
Or those which technically cannot be represented in any other way.

URL
---
Every URL ``MUST`` follow the general guideline of :ref:`naming`.
Besides, a URL ``MUST NOT`` end with a trailing slash.

Methods
-------
The API ``MUST`` only provide the methods necessary for the situation.
This ``SHOULD`` be implemented strictly according to `RFC 7231<https://tools.ietf.org/html/rfc7231>`_.

+--------+---------------------------------------------------------+---------------+---------------+
| Method | Description                                             | HTTP Response | Is Idempotent |
+========+=========================================================+===============+===============+
| GET    | Returns a resource or collection.                       | 200           | True          |
+--------+---------------------------------------------------------+---------------+---------------+
| POST   | Adds a new resource.                                    | 201           | False         |
+--------+---------------------------------------------------------+---------------+---------------+
| PUT    | Replaces a resource.                                    | 200           | True          |
+--------+---------------------------------------------------------+---------------+---------------+
| PATCH  | Modifies a resource.                                    | 200           | False         |
+--------+---------------------------------------------------------+---------------+---------------+
| DELETE | Delets a ressource or collection                        | 202           | True          |
+--------+---------------------------------------------------------+---------------+---------------+
| HEAD   | Returns meta information about a resource or collection | 200           | True          |
+--------+---------------------------------------------------------+---------------+---------------+

Parameters
----------
Parameters should always be available via query string as described in `RFC 3986 <https://tools.ietf.org/html/rfc3986>`_.
Parameters are the only elements for which :ref:`naming` is ``OPTIONAL``.

Filtering
---------
Most collections ``SHOULD`` have the ability to filter.
The parameter filter is used as an identifier.

- Chained statements are linked using commas (,).
- Nested elements are described using a period (.).

Sorting
-------
To use sort rules, the parameter sort ``MUST`` be used.
Customize complex sort requirements by letting the sort parameter include a list of comma-separated fields,
each containing a possible negative signifying a descending sort order.

- Default sort requirement is the public id
- Default sort order is ascending

Pagination
----------
Pagination over a collection ``SHOULD`` be supported using the Link header described by `RFC 5988 <https://tools.ietf.org/html/rfc5988>`_.
The default maximum number of resources returned ``SHOULD`` be 10, but ``MAY`` be changed over the parameters.

Documentation
-------------
Each resource, collection and route ``MUST`` be described technically.
This ``MUST`` contain the identifier, possible error messages, a description of the successful response and, depending on the HTTP method, a request example.

Responses
=========

Status Codes
------------
You ``MUST`` use HTTP status codes to make conclusions about the type of response.
The available status codes are defined in `RFC7231 <https://tools.ietf.org/html/rfc7231>`_.
Status codes important for the API are:

2xx Success
^^^^^^^^^^^
The request was successful, the answer can be used.

:200 OK:
    The request was successfully processed and the result of the request is transferred in the response.
:201 Created:
    The request was successfully processed. The requested resource was created before the response was sent. The **Location** header field ``MAY`` contain the address of the created resource.
:202 Accepted:
    The request was accepted but will be executed at a later date. The success of the request cannot be guaranteed.
:204 No Content:
    The request was successful, but the answer deliberately contains no data.
:205 Reset Content:
    The request was successful; the client should rebuild the document and reset form inputs.
:206 Partial Content:
    The requested part has been successfully transferred (used in connection with a "Content-Range" header field or the content type multipart/byteranges). Can inform a client about partial downloads.

3xx Redirection
^^^^^^^^^^^^^^^
To ensure a successful processing of the request, further steps on the part of the client are necessary.

:300 Multiple Choices:
     The requested resource is available in different ways. The response contains a list of the available types. The "Location" header field may contain the address of the server's preferred representation.
:301 Moved Permanently:
    The requested resource is now available at the address given in the "Location" header field (also called redirect). The old address is no longer valid.
:304 Not Modified:
    The content of the requested resource has not changed since the last query of the client and is therefore not transferred.

4xx Client errors
^^^^^^^^^^^^^^^^^
The cause of the failure of the request is probably the responsibility of the client.

:400 Bad Request:
    The request message was structured incorrectly.
:401 Unauthorized:
    The request cannot be made without valid authentication. How the authentication is to be performed is transmitted in the "WWW-Authenticate" header field of the response.
:403 Forbidden:
    The request was not executed due to lack of client authorization, e.g. because the authenticated user is not authorized, or a URL configured as HTTPS was only called with HTTP.
:404 Not Found:
    The requested resource was not found. This status code can ``OPTIONAL`` also be used to reject a request without further explanation.
:405 Method Not Allowed:
    The request can only be made using other HTTP methods. Valid methods for the resource in question are transmitted in the "Allow" header field of the response.
:406 Not Acceptable:
    The requested resource is not available in the desired form. Valid "Content-Type" values can be transmitted in the reply.
:409 Conflict:
    The request was made under false assumptions. In the case of a PUT request, for example, this may be due to a change in the resource by a third party in the meantime.
:410 Gone:
    The requested resource is no longer provided and has been permanently removed.
:423 Locked:
    The requested resource is currently locked.

5xx Server errors
^^^^^^^^^^^^^^^^^
Not clearly distinguishable from the so-called client errors. However, the cause of the failure of the request is probably the responsibility of the server.

:500 Internal Server Error:
    This is a "summary status code" for unexpected server errors.
:501 Not Implemented:
    The functionality to process the request is not provided by this server. The cause is, for example, an unknown or unsupported HTTP method.

Error Codes
-----------
Errors ``MUST`` be returned with the respective HTTP status code as abort (4xx-5xx).
The message ``SHOULD`` contain the following information (unless explicitly stated otherwise).

:Status:
    HTTP Status Code.
:Response:
    Url or identifier which threw the error.
:Description:
    Short description of the error class/module
:Message:
    ``OPTIONAL`` A precisely formulated message about the error, possible causes or further action.

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
