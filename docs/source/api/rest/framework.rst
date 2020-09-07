Framework
=========

Category
--------

.. http:get:: /rest/categories/

       HTTP GET/HEAD rest route. HEAD will be the same result except their will be no body.

       **Example request**:

       .. sourcecode:: http

          GET /rest/categories/ HTTP/1.1
          Host: datagerry.com
          Accept: application/json

       **Example response**:

       .. sourcecode:: http

          HTTP/1.1 200 OK
          Content-Type: application/json
          Content-Length: 3311
          X-Total-Count: 1
          X-API-Version: 1.0

          {
              "results": [
                {
                  "public_id": 1,
                  "name": "example",
                  "label": "Example",
                  "meta": {
                    "icon": "",
                    "order": null
                  },
                  "parent": null,
                  "types": [1]
                }
              ],
              "count": 1,
              "total": 1,
              "parameters": {
                "limit": 10,
                "sort": "public_id",
                "order": 1,
                "page": 1,
                "filter": {},
                "optional": {
                  "view": "list"
                }
              },
              "pager": {
                "page": 1,
                "page_size": 10,
                "total_pages": 1
              },
              "pagination": {
                "current": "http://localhost:4000/rest/categories/",
                "first": "http://localhost:4000/rest/categories/?page=1",
                "prev": "http://localhost:4000/rest/categories/?page=1",
                "next": "http://localhost:4000/rest/categories/?page=1",
                "last": "http://localhost:4000/rest/categories/?page=1"
              },
              "response_type": "GET",
              "model": "Category",
              "time": "2020-08-20T10:13:15.350747"
            }

       :query sort: the sort field name. default is public_id
       :query order: the sort order value for ascending or descending. default is 1 for ascending
       :query page: the current view page. default is 1
       :query limit: max number of results. default is 10
       :query filter: a mongodb query filter. default is {} which means everything
       :query view: the category view data-structure. Can be `list` or `tree`. default is `list`

       :reqheader Accept: application/json
       :reqheader Authorization: jwtoken to authenticate
       :resheader Content-Type: application/json
       :statuscode 200: Everything is fine.
       :statuscode 400: The request or the parameters are wrong formatted.
       :statuscode 404: No collection or resources found.

.. http:get:: /category/(int:public_id)

        The category with the public_id.

        **Example request**

        .. sourcecode:: http

            GET /rest/categories/1 HTTP/1.1
            Host: datagerry.com
            Accept: application/json

        **Example response**

        .. sourcecode:: http

            HTTP/1.1 200 OK
            Content-Type: application/json
            Content-Length: 588
            X-API-Version: 1.0

            {
              "result": {
                "public_id": 1,
                "name": "example",
                "label": "Example",
                "meta": {
                  "icon": "far fa-folder-open",
                  "order": 0
                },
                "parent": null,
                "types": [1]
              },
              "response_type": "GET",
              "model": "Category",
              "time": "2020-08-20T09:21:10.235525"
            }

        :reqheader Accept: application/json
        :reqheader Authorization: jwtoken to authenticate
        :resheader Content-Type: application/json
        :statuscode 200: Everything is fine.
        :statuscode 404: No resource found.

.. http:post:: /category/

        HTTP Post route for inserting a new category.

        **Example request**

        .. sourcecode:: http

            POST /rest/categories/ HTTP/1.1
            Host: datagerry.com
            Accept: application/json

            {
              "name": "example",
              "label": "Example",
              "meta": {
                "icon": "",
                "order": 0
              },
              "parent": null,
              "types": [1]
            }

        **Example response**

        .. sourcecode:: http

            HTTP/1.1 200 OK
            Content-Type: application/json
            Content-Length: 588
            Location: http://localhost:4000/rest/categories/1
            X-API-Version: 1.0

            {
              "result_id": 1,
              "raw": {
                "public_id": 1,
                "name": "example",
                "label": "Example",
                "meta": {
                  "icon": "",
                  "order": 0
                },
                "parent": null,
                "types": [1]
              },
              "response_type": "INSERT",
              "model": "Category",
              "time": "2020-08-20T11:14:42.704920"
            }

        :reqheader Accept: application/json
        :reqheader Authorization: jwtoken to authenticate
        :resheader Content-Type: application/json
        :statuscode 200: Everything is fine.
        :statuscode 400: Resource could not be inserted.
        :statuscode 404: No resource found.

.. http:put:: /category/(int:public_id)

        HTTP `PUT`/`PATCH` route for updating a existing category.

        **Example request**

        .. sourcecode:: http

            PUT /rest/categories/1 HTTP/1.1
            Host: datagerry.com
            Accept: application/json

            {
              ""public_id": 1,
              "name": "example",
              "label": "Example",
              "meta": {
                "icon": "",
                "order": 0
              },
              "parent": null,
              "types": [1]
            }

        **Example response**

        .. sourcecode:: http

            HTTP/1.1 202 ACCEPTED
            Content-Type: application/json
            Content-Length: 170
            Location: http://localhost:4000/rest/categories/1
            X-API-Version: 1.0

            {
              "result": {
                "public_id": 1,
                "name": "example2",
                "label": "Example,
                "meta": {
                  "icon": "",
                  "order": 0
                },
                "parent": null,
                "types": []
              },
              "response_type": "UPDATE",
              "model": "Category",
              "time": "2020-08-20T11:37:07.499137"
            }

        :reqheader Accept: application/json
        :reqheader Authorization: jwtoken to authenticate
        :resheader Content-Type: application/json
        :statuscode 202: Everything is fine.
        :statuscode 400: Resource could not be updated.
        :statuscode 404: No resource found.

.. http:delete:: /category/(int:public_id)

        HTTP `DELETE` route for deleting a existing category.

        **Example request**

        .. sourcecode:: http

            DELETE /rest/categories/1 HTTP/1.1
            Host: datagerry.com
            Accept: application/json

        **Example response**

        .. sourcecode:: http

            HTTP/1.1 202 ACCEPTED
            Content-Type: application/json
            Content-Length: 170
            X-API-Version: 1.0

            {
              "deleted_entry": {
                "public_id": 1,
                "name": "example",
                "label": "Example",
                "meta": {
                  "icon": "",
                  "order": 1
                },
                "parent": null,
                "types": [
                  1
                ]
              },
              "response_type": "DELETE",
              "model": "Category",
              "time": "2020-08-20T11:45:50.809706"
            }

        :reqheader Accept: application/json
        :reqheader Authorization: jwtoken to authenticate
        :resheader Content-Type: application/json
        :statuscode 202: Everything is fine.
        :statuscode 400: Resource could not be deleted.
        :statuscode 404: No resource found.