User Management
===============

.. contents::
    :depth: 3

Users
-----

.. http:get:: /users/

        HTTP `GET/HEAD` rest route. HEAD will be the same result except their will be no body.

        **Example request**:

        .. sourcecode:: http

            GET /rest/users/ HTTP/1.1
            Host: datagerry.com
            Accept: application/json

        **Example response**:

        .. sourcecode:: http

            HTTP/1.1 200 OK
            Content-Type: application/json
            Content-Length: 1000
            X-Total-Count: 1
            X-API-Version: 1.0

            {
               "results": [
                    {
                      "public_id": 1,
                      "user_name": "admin",
                      "active": true,
                      "group_id": 1,
                      "registration_time": "2020-01-01 00:00:00.000000",
                      "authenticator": "LocalAuthenticationProvider",
                      "email": null,
                      "password": "YWJjZGVmZ2hpamtsbW5vcHFyc3R1dnd4eXo=",
                      "image": null,
                      "first_name": null,
                      "last_name": null
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
                "optional": {}
              },
              "pager": {
                "page": 1,
                "page_size": 10,
                "total_pages": 1
              },
              "pagination": {
                "current": "http://datagerry.com/rest/users/",
                "first": "http://datagerry.com/rest/users/?page=1",
                "prev": "http://datagerry.com/rest/users/?page=1",
                "next": "http://datagerry.com/rest/users/?page=1",
                "last": "http://datagerry.com/rest/users/?page=1"
              },
              "response_type": "GET",
              "model": "User",
              "time": "2020-01-01 00:00:00.000000"
            }

        :query sort: the sort field name. default is public_id
        :query order: the sort order value for ascending or descending. default is 1 for ascending
        :query page: the current view page. default is 1
        :query limit: max number of results. default is 10
        :query filter: a mongodb query filter. default is {} which means everything

        :reqheader Accept: application/json
        :reqheader Authorization: jwtoken to authenticate
        :resheader Content-Type: application/json
        :statuscode 200: Everything is fine.
        :statuscode 400: The request or the parameters are wrong formatted.
        :statuscode 404: No collection or resources found.

.. http:get:: /users/(int:public_id)

        HTTP `GET/HEAD` rest route for a single resource by its ID.

        **Example request**

        .. sourcecode:: http

            GET /rest/users/1 HTTP/1.1
            Host: datagerry.com
            Accept: application/json

        **Example response**

        .. sourcecode:: http

            HTTP/1.1 200 OK
            Content-Type: application/json
            Content-Length: 100
            X-API-Version: 1.0

            {
                "result": {
                    "public_id": 1,
                    "user_name": "admin",
                    "active": true,
                    "group_id": 1,
                    "registration_time": "2020-01-01 00:00:00.000000",
                    "authenticator": "LocalAuthenticationProvider",
                    "email": null,
                    "password": "YWJjZGVmZ2hpamtsbW5vcHFyc3R1dnd4eXo=",
                    "image": null,
                    "first_name": null,
                    "last_name": null
                },
                "response_type": "GET",
                "model": "User",
                "time": "2020-01-01 00:00:00.000000"
            }

        :reqheader Accept: application/json
        :reqheader Authorization: jwtoken to authenticate
        :resheader Content-Type: application/json
        :statuscode 200: Everything is fine.
        :statuscode 404: No resource found.

.. http:post:: /users/

        HTTP `POST` route for inserting a new user.

        **Example request**

        .. sourcecode:: http

            POST /rest/users/ HTTP/1.1
            Host: datagerry.com
            Accept: application/json

            {
                "user_name": "test",
                "active": true,
                "group_id": 2,
                "password": "YWJjZGVmZ2hpamtsbW5vcHFyc3R1dnd4eXo=",
            }

        **Example response**

        .. sourcecode:: http

            HTTP/1.1 200 OK
            Content-Type: application/json
            Content-Length: 100
            Location: http://datagerry.com/rest/users/2
            X-API-Version: 1.0

            {
              "result_id": 2,
              "raw": {
                    "public_id": 2,
                    "user_name": "test",
                    "active": true,
                    "group_id": 2,
                    "registration_time": "2020-01-01 00:00:00.000000",
                    "authenticator": "LocalAuthenticationProvider",
                    "email": null,
                    "password": "YWJjZGVmZ2hpamtsbW5vcHFyc3R1dnd4eXo=",
                    "image": null,
                    "first_name": null,
                    "last_name": null
                },
              "response_type": "INSERT",
              "model": "User",
              "time": "1970-01-01T00:00:00"
            }

        :reqheader Accept: application/json
        :reqheader Authorization: jwtoken to authenticate
        :resheader Content-Type: application/json
        :statuscode 201: Resource was created.
        :statuscode 400: Resource could not be inserted.
        :statuscode 404: No resource found.

.. http:put:: /users/(int:public_id)

        HTTP `PUT`/`PATCH` route for updating a existing user.

        **Example request**

        .. sourcecode:: http

            PUT /rest/users/1 HTTP/1.1
            Host: datagerry.com
            Accept: application/json

            {
                "public_id": 1,
                "user_name": "admin",
                "active": false,
                "group_id": 1,
                "registration_time": "2020-01-01 00:00:00.000000",
                "authenticator": "LocalAuthenticationProvider",
                "email": null,
                "password": "YWJjZGVmZ2hpamtsbW5vcHFyc3R1dnd4eXo=",
                "image": null,
                "first_name": null,
                "last_name": null
            }

        **Example response**

        .. sourcecode:: http

            HTTP/1.1 202 ACCEPTED
            Content-Type: application/json
            Content-Length: 100
            Location: http://datagerry.com/rest/users/1
            X-API-Version: 1.0

            {
                "result": {
                    "public_id": 1,
                    "user_name": "admin",
                    "active": false,
                    "group_id": 1,
                    "registration_time": "2020-01-01 00:00:00.000000",
                    "authenticator": "LocalAuthenticationProvider",
                    "email": null,
                    "password": "YWJjZGVmZ2hpamtsbW5vcHFyc3R1dnd4eXo=",
                    "image": null,
                    "first_name": null,
                    "last_name": null
                },
                "response_type": "UPDATE",
                "model": "User",
                "time": "2020-01-01 00:00:00.000000"
            }

        :reqheader Accept: application/json
        :reqheader Authorization: jwtoken to authenticate
        :resheader Content-Type: application/json
        :statuscode 202: Everything is fine.
        :statuscode 400: Resource could not be updated.
        :statuscode 404: No resource found.

.. http:delete:: /users/(int:public_id)

        HTTP `DELETE` route for deleting a existing user.

        **Example request**

        .. sourcecode:: http

            DELETE /rest/users/1 HTTP/1.1
            Host: datagerry.com
            Accept: application/json

        **Example response**

        .. sourcecode:: http

            HTTP/1.1 202 ACCEPTED
            Content-Type: application/json
            Content-Length: 100
            X-API-Version: 1.0

            {
                "deleted_entry": {
                    "public_id": 1,
                    "user_name": "admin",
                    "active": false,
                    "group_id": 1,
                    "registration_time": "2020-01-01 00:00:00.000000",
                    "authenticator": "LocalAuthenticationProvider",
                    "email": null,
                    "password": "YWJjZGVmZ2hpamtsbW5vcHFyc3R1dnd4eXo=",
                    "image": null,
                    "first_name": null,
                    "last_name": null
                },
              "response_type": "DELETE",
              "model": "User",
              "time": "2020-01-01 00:00:00.000000"
            }

        :reqheader Accept: application/json
        :reqheader Authorization: jwtoken to authenticate
        :resheader Content-Type: application/json
        :statuscode 202: Everything is fine.
        :statuscode 400: Resource could not be deleted.
        :statuscode 404: No resource found.

Groups
------

.. http:get:: /groups/

        HTTP `GET/HEAD` rest route. HEAD will be the same result except their will be no body.

        **Example request**:

        .. sourcecode:: http

            GET /rest/groups/ HTTP/1.1
            Host: datagerry.com
            Accept: application/json

        **Example response**:

        .. sourcecode:: http

            HTTP/1.1 200 OK
            Content-Type: application/json
            Content-Length: 1000
            X-Total-Count: 1
            X-API-Version: 1.0

            {
               "results": [
                    {
                        "public_id": 1,
                        "name": "admin",
                        "label": "Administrator",
                        "rights": [
                            {
                                "level": 0,
                                "name": "base.*",
                                "label": "base.*",
                                "description": "Base application right",
                                "is_master": true
                            }
                        ]
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
                "optional": {}
              },
              "pager": {
                "page": 1,
                "page_size": 10,
                "total_pages": 1
              },
              "pagination": {
                "current": "http://datagerry.com/rest/groups/",
                "first": "http://datagerry.com/rest/groups/?page=1",
                "prev": "http://datagerry.com/rest/groups/?page=1",
                "next": "http://datagerry.com/rest/groups/?page=1",
                "last": "http://datagerry.com/rest/groups/?page=1"
              },
              "response_type": "GET",
              "model": "Group",
              "time": "2020-01-01 00:00:00.000000"
            }

        :query sort: the sort field name. default is public_id
        :query order: the sort order value for ascending or descending. default is 1 for ascending
        :query page: the current view page. default is 1
        :query limit: max number of results. default is 10
        :query filter: a mongodb query filter. default is {} which means everything

        :reqheader Accept: application/json
        :reqheader Authorization: jwtoken to authenticate
        :resheader Content-Type: application/json
        :statuscode 200: Everything is fine.
        :statuscode 400: The request or the parameters are wrong formatted.
        :statuscode 404: No collection or resources found.

.. http:get:: /groups/(int:public_id)

        HTTP `GET/HEAD` rest route for a single resource by its ID.

        **Example request**

        .. sourcecode:: http

            GET /rest/groups/1 HTTP/1.1
            Host: datagerry.com
            Accept: application/json

        **Example response**

        .. sourcecode:: http

            HTTP/1.1 200 OK
            Content-Type: application/json
            Content-Length: 100
            X-API-Version: 1.0

            {
                "result": {
                    "public_id": 1,
                    "name": "admin",
                    "label": "Administrator",
                    "rights": [
                        {
                            "level": 0,
                            "name": "base.*",
                            "label": "base.*",
                            "description": "Base application right",
                            "is_master": true
                        }
                    ]
                },
                "response_type": "GET",
                "model": "Group",
                "time": "2020-01-01 00:00:00.000000"
            }

        :reqheader Accept: application/json
        :reqheader Authorization: jwtoken to authenticate
        :resheader Content-Type: application/json
        :statuscode 200: Everything is fine.
        :statuscode 404: No resource found.

.. http:post:: /groups/

        HTTP `POST` route for inserting a new group.

        **Example request**

        .. sourcecode:: http

            POST /rest/groups/ HTTP/1.1
            Host: datagerry.com
            Accept: application/json

            {
                "name": "test",
                "label": "test",
                "rights": [
                    "base.framework.object.*"
                ]
            }

        **Example response**

        .. sourcecode:: http

            HTTP/1.1 200 OK
            Content-Type: application/json
            Content-Length: 100
            Location: http://datagerry.com/rest/groups/3
            X-API-Version: 1.0

            {
                "result_id": 3,
                "raw": {
                    "public_id": 3,
                    "name": "test",
                    "label": "test",
                    "rights": [
                        {
                            "level": 10,
                            "name": "base.framework.object.*",
                            "label": "object.*",
                            "description": "Manage objects from framework",
                            "is_master": true
                        }
                    ]
                },
                "response_type": "INSERT",
                "model": "Group",
                "time": "2020-01-01 00:00:00.000000"
            }

        :reqheader Accept: application/json
        :reqheader Authorization: jwtoken to authenticate
        :resheader Content-Type: application/json
        :statuscode 201: Resource was created.
        :statuscode 400: Resource could not be inserted.
        :statuscode 404: No resource found.

.. http:put:: /groups/(int:public_id)

        HTTP `PUT`/`PATCH` route for updating a existing user.

        **Example request**

        .. sourcecode:: http

            PUT /rest/groups/3 HTTP/1.1
            Host: datagerry.com
            Accept: application/json

            {
                "public_id": 3,
                "name": "test",
                "label": "Test",
                "rights": [
                    "base.framework.object.*"
                ]
            }

        **Example response**

        .. sourcecode:: http

            HTTP/1.1 202 ACCEPTED
            Content-Type: application/json
            Content-Length: 100
            Location: http://datagerry.com/rest/groups/3
            X-API-Version: 1.0

            {
                "result": {
                    "public_id": 3,
                    "name": "test",
                    "label": "Test",
                    "rights": [
                        "base.framework.object.*"
                    ]
                },
                "response_type": "UPDATE",
                "model": "Group",
                "time": "2020-01-01 00:00:00.000000"
            }

        :reqheader Accept: application/json
        :reqheader Authorization: jwtoken to authenticate
        :resheader Content-Type: application/json
        :statuscode 202: Everything is fine.
        :statuscode 400: Resource could not be updated.
        :statuscode 404: No resource found.

.. http:delete:: /groups/(int:public_id)

        HTTP `DELETE` route for deleting a existing user.

        .. note::
            Group with PublicID 1 (Admin) & 2 (User) can not be deleted!

        **Example request**

        .. sourcecode:: http

            DELETE /rest/groups/3 HTTP/1.1
            Host: datagerry.com
            Accept: application/json

        **Example response**

        .. sourcecode:: http

            HTTP/1.1 202 ACCEPTED
            Content-Type: application/json
            Content-Length: 100
            X-API-Version: 1.0

            {
                "deleted_entry":  {
                    "public_id": 3,
                    "name": "test",
                    "label": "Test",
                    "rights": [
                        {
                            "level": 10,
                            "name": "base.framework.object.*",
                            "label": "object.*",
                            "description": "Manage objects from framework",
                            "is_master": true
                        }
                    ]
                },
                "response_type": "DELETE",
                "model": "Group",
                "time": "2020-01-01 00:00:00.000000"
            }

        :query action: Parameter of GroupDeleteMode. `MOVE` will push all users in this group to passed `group_id`
                        and `DELETE` will delete all users in this group.
        :query group_id: The PublicID of the group which the `MOVE` action will be use.

        :reqheader Accept: application/json
        :reqheader Authorization: jwtoken to authenticate
        :resheader Content-Type: application/json
        :statuscode 202: Everything is fine.
        :statuscode 400: Resource could not be deleted.
        :statuscode 404: No resource found.

Rights
------

.. note::
    The right routes are static.

.. http:get:: /rights/

        HTTP `GET/HEAD` rest route. HEAD will be the same result except their will be no body.

        **Example request**:

        .. sourcecode:: http

            GET /rest/rights/ HTTP/1.1
            Host: datagerry.com
            Accept: application/json

        **Example response**:

        {
           "results":[
              {
                 "level":0,
                 "name":"base.*",
                 "label":"base.*",
                 "description":"Base application right",
                 "is_master":true
              },
              {
                 "level":50,
                 "name":"base.docapi.*",
                 "label":"docapi.*",
                 "description":"Manage DocAPI",
                 "is_master":true
              },
              {
                 "level":50,
                 "name":"base.docapi.template.*",
                 "label":"template.*",
                 "description":"Manage DocAPI templates",
                 "is_master":true
              },
              {
                 "level":50,
                 "name":"base.docapi.template.add",
                 "label":"template.add",
                 "description":"Add template",
                 "is_master":false
              },
              {
                 "level":50,
                 "name":"base.docapi.template.delete",
                 "label":"template.delete",
                 "description":"Delete template",
                 "is_master":false
              },
              {
                 "level":50,
                 "name":"base.docapi.template.edit",
                 "label":"template.edit",
                 "description":"Edit template",
                 "is_master":false
              },
              {
                 "level":50,
                 "name":"base.docapi.template.view",
                 "label":"template.view",
                 "description":"View template",
                 "is_master":false
              },
              {
                 "level":50,
                 "name":"base.export.*",
                 "label":"export.*",
                 "description":"Manage exports",
                 "is_master":true
              },
              {
                 "level":50,
                 "name":"base.export.object.*",
                 "label":"object.*",
                 "description":"Manage object exports",
                 "is_master":true
              },
              {
                 "level":50,
                 "name":"base.export.type.*",
                 "label":"type.*",
                 "description":"Manage type exports",
                 "is_master":true
              }
           ],
           "count":10,
           "total":62,
           "parameters":{
              "limit":10,
              "sort":"name",
              "order":1,
              "page":1,
              "filter":{

              },
              "optional":{
                 "view":"list"
              }
           },
           "pager":{
              "page":1,
              "page_size":10,
              "total_pages":7
           },
           "pagination":{
              "current":"http://datagerry.com/rest/rights/",
              "first":"http://datagerry.com/rest/rights/?page=1",
              "prev":"http://datagerry.com/rest/rights/?page=1",
              "next":"http://datagerry.com/rest/rights/?page=2",
              "last":"http://datagerry.com/rest/rights/?page=7"
           },
           "response_type":"GET",
           "model":"Right",
           "time":"2020-01-01 00:00:00.000000"
        }

        :query sort: the sort field name. default is `name`.
        :query order: the sort order value for ascending or descending. default is 1 for ascending
        :query page: the current view page. default is 1
        :query limit: max number of results. default is 10
        :query filter: a mongodb query filter. default is {} which means everything
        :query optional: `view` parameter. Default is list.

        :reqheader Accept: application/json
        :reqheader Authorization: jwtoken to authenticate
        :resheader Content-Type: application/json
        :statuscode 200: Everything is fine.
        :statuscode 400: The request or the parameters are wrong formatted.
        :statuscode 404: No collection or resources found.

.. http:get:: /rights/(str:name)

        HTTP `GET/HEAD` rest route for a single resource by its name.

        **Example request**

        .. sourcecode:: http

            GET /rest/rights/base.* HTTP/1.1
            Host: datagerry.com
            Accept: application/json

        **Example response**

        .. sourcecode:: http

            HTTP/1.1 200 OK
            Content-Type: application/json
            Content-Length: 100
            X-API-Version: 1.0

            {
                "result": {
                    "level": 0,
                    "name": "base.*",
                    "label": "base.*",
                    "description": "Base application right",
                    "is_master": true
                },
                "response_type": "GET",
                "model": "Right",
                "time": "2020-01-01 00:00:00.000000"
            }

        :reqheader Accept: application/json
        :reqheader Authorization: jwtoken to authenticate
        :resheader Content-Type: application/json
        :statuscode 200: Everything is fine.
        :statuscode 404: No resource found.

.. http:get:: /rights/levels

        HTTP `GET/HEAD` rest route for a all security levels.

        **Example request**

        .. sourcecode:: http

            GET /rest/rights/levels HTTP/1.1
            Host: datagerry.com
            Accept: application/json

        **Example response**

        .. sourcecode:: http

            HTTP/1.1 200 OK
            Content-Type: application/json
            Content-Length: 100
            X-API-Version: 1.0

            {
              "result": {
                "CRITICAL": 100,
                "DANGER": 80,
                "SECURE": 50,
                "PROTECTED": 30,
                "PERMISSION": 10,
                "NOTSET": 0
              },
              "response_type": "GET",
              "model": "Security-Level",
              "time": "2020-01-01 00:00:00.000000"
            }

        :reqheader Accept: application/json
        :reqheader Authorization: jwtoken to authenticate
        :resheader Content-Type: application/json
        :statuscode 200: Everything is fine.


Settings
--------

.. http:get:: /users/(int:user_id)/settings/

        HTTP `GET/HEAD` rest route. HEAD will be the same result except their will be no body.

        **Example request**:

        .. sourcecode:: http

            GET /rest/users/1/settings/ HTTP/1.1
            Host: datagerry.com
            Accept: application/json

        **Example response**:

        .. sourcecode:: http

            HTTP/1.1 200 OK
            Content-Type: application/json
            Content-Length: 1000
            X-Total-Count: 1
            X-API-Version: 1.0

            {
              "results": [
                {
                  "identifier": "test",
                  "user_id": 1,
                  "payload": {},
                  "setting_type": "GLOBAL"
                }
              ],
              "response_type": "GET",
              "model": "UserSetting",
              "time": "2020-01-01 00:00:00.000000"
            }

        :reqheader Accept: application/json
        :reqheader Authorization: jwtoken to authenticate
        :resheader Content-Type: application/json
        :statuscode 200: Everything is fine.
        :statuscode 400: The request or the parameters are wrong formatted.
        :statuscode 404: No collection or resources found.

.. http:get:: /users/(int:public_id)/settings/(str:identifier)

        HTTP `GET/HEAD` rest route for a single resource by the UserID and the setting identifier.

        **Example request**

        .. sourcecode:: http

            GET /rest/users/1/settings/test HTTP/1.1
            Host: datagerry.com
            Accept: application/json

        **Example response**

        .. sourcecode:: http

            HTTP/1.1 200 OK
            Content-Type: application/json
            Content-Length: 100
            X-API-Version: 1.0

            {
              "results": [
                {
                  "identifier": "test",
                  "user_id": 1,
                  "payload": {},
                  "setting_type": "GLOBAL"
                }
              ],
              "response_type": "GET",
              "model": "UserSetting",
              "time": "2020-01-01 00:00:00.000000"
            }

        :reqheader Accept: application/json
        :reqheader Authorization: jwtoken to authenticate
        :resheader Content-Type: application/json
        :statuscode 200: Everything is fine.
        :statuscode 404: No resource found.

.. http:post:: /users/(int:public_id)/settings/

        HTTP `POST` route for inserting a new setting.

        **Example request**

        .. sourcecode:: http

            POST /rest/users/1/settings/ HTTP/1.1
            Host: datagerry.com
            Accept: application/json

            {
                "identifier" : "test",
                "user_id" : 1,
                "payload" : {},
                "setting_type" : "GLOBAL"
            }

        **Example response**

        .. sourcecode:: http

            HTTP/1.1 201 CREATED
            Content-Type: application/json
            Content-Length: 100
            Location: http://datagerry.com/rest/users/1/settings/test
            X-API-Version: 1.0

            {
              "result_id": "test",
              "raw": {
                "identifier": "test",
                "user_id": 1,
                "payload": {},
                "setting_type": "GLOBAL"
              },
              "response_type": "INSERT",
              "model": "UserSetting",
              "time": "2020-01-01 00:00:00.000000"
            }

        :reqheader Accept: application/json
        :reqheader Authorization: jwtoken to authenticate
        :resheader Content-Type: application/json
        :statuscode 201: Resource was created.
        :statuscode 400: Resource could not be inserted.
        :statuscode 404: No resource found.

.. http:put:: /users/(int:public_id)/settings/(str:identifier)

        HTTP `PUT`/`PATCH` route for updating a setting.

        **Example request**

        .. sourcecode:: http

            PUT /rest/users/1/settings/test HTTP/1.1
            Host: datagerry.com
            Accept: application/json

            {
                "identifier" : "test",
                "user_id" : 1,
                "payload" : {},
                "setting_type" : "GLOBAL"
            }

        **Example response**

        .. sourcecode:: http

            HTTP/1.1 202 ACCEPTED
            Content-Type: application/json
            Content-Length: 100
            Location: http://datagerry.com/rest/users/1/settings/test
            X-API-Version: 1.0

            {
                "result": {
                    "identifier": "test",
                    "user_id": 1,
                    "payload": {},
                    "setting_type": "GLOBAL"
                },
                "response_type": "UPDATE",
                "model": "UserSetting",
                "time": "2020-01-01 00:00:00.000000"
            }

        :reqheader Accept: application/json
        :reqheader Authorization: jwtoken to authenticate
        :resheader Content-Type: application/json
        :statuscode 202: Everything is fine.
        :statuscode 400: Resource could not be updated.
        :statuscode 404: No resource found.

.. http:delete:: /users/(int:public_id)/settings/(str:identifier)

        HTTP `DELETE` route for deleting a existing setting.

        **Example request**

        .. sourcecode:: http

            DELETE /rest/users/1/settings/test HTTP/1.1
            Host: datagerry.com
            Accept: application/json

        **Example response**

        .. sourcecode:: http

            HTTP/1.1 202 ACCEPTED
            Content-Type: application/json
            Content-Length: 100
            X-API-Version: 1.0

            {
                "deleted_entry": {
                    "identifier": "test",
                    "user_id": 1,
                    "payload": {},
                    "setting_type": "APPLICATION"
                },
                "response_type": "DELETE",
                "model": "UserSetting",
                "time": "2020-01-01 00:00:00.000000"
            }

        :reqheader Accept: application/json
        :reqheader Authorization: jwtoken to authenticate
        :resheader Content-Type: application/json
        :statuscode 202: Everything is fine.
        :statuscode 400: Resource could not be deleted.
        :statuscode 404: No resource found.