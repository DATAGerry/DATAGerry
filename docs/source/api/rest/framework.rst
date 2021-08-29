Framework
=========

For the creation and editing of datasets in DATAGERRY certain validation schemes are followed.
For the validation of the datasets the Python library 'Cerberus_' is used. A validation schema is a mapping,
usually a dict. Schema keys are the keys allowed in the target dictionary.
Schema values express the rules that must match the corresponding target values.

.. _Cerberus: https://docs.python-cerberus.org/en/stable/

Objects
-------
Create and manage your first objects via the Rest-API

READ (GET) - Operation
^^^^^^^^^^^^^^^^^^^^^^

Overview of all GET routes to get objects from the database.

.. http:get:: /objects/

        Returns a collection of objects in different formats. HTTP `GET/HEAD` rest route.
        `HEAD` will be the same result except their will be no body.

        **Example request**:

        .. sourcecode:: http

            GET /rest/objects/ HTTP/1.1
            Host: datagerry.com
            Accept: application/json

        **Example response**:

        .. sourcecode:: http

            HTTP/1.1 200 OK
            Content-Type: application/json
            X-Total-Count: 1
            X-API-Version: 1.0

            {
                  "results": [
                    {
                      "public_id": 1
                      "type_id": 1,
                      "status": null,
                      "version": "1.0.0",
                      "creation_time": "1970-01-01T00:00:00.000000",
                      "author_id": 1,
                      "last_edit_time": "1970-01-01T00:00:00.000000",
                      "editor_id": 1,
                      "active": true,
                      "fields": [
                        {
                          "name": "example",
                          "value": "value"
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
                    "current": "http://datagerry.com/rest/objects/",
                    "first": "http://datagerry.com/rest/objects/?page=1",
                    "prev": "http://datagerry.com/rest/objects/?page=1",
                    "next": "http://datagerry.com/rest/objects/?page=1",
                    "last": "http://datagerry.com/rest/objects/?page=1"
                  },
                  "response_type": "GET",
                  "model": "Object",
                  "time": "1970-01-01T00:00:00.000000"
            }

        :query view: Return view of the response. Values `native` or `render`. Default is `native`.
        :query active: Show only active objects. Could also be set over the filter.
        :query sort: the sort field name. default is public_id
        :query order: the sort order value for ascending or descending. Default is 1 for ascending.
        :query page: the current view page. default is 1
        :query limit: max number of results. default is 10
        :query filter: a mongodb query filter. default is {} which means everything
        :query projection: a mongodb project filter.

        :reqheader Accept: application/json
        :reqheader Authorization: JW-Token to authenticate
        :resheader Content-Type: application/json
        :statuscode 200: Everything is fine.
        :statuscode 400: The request or the parameters are wrong formatted.
        :statuscode 404: No collection or resources found.

.. http:get:: /objects/(int:public_id)

        Returns a rendered object. HTTP `GET/HEAD` rest route.
        `HEAD` will be the same result except their will be no body.

        **Example request**:

        .. sourcecode:: http

            GET /rest/objects/1 HTTP/1.1
            Host: datagerry.com
            Accept: application/json

        **Example response**:

        .. sourcecode:: http

            HTTP/1.1 200 OK
            Content-Type: application/json
            X-Total-Count: 1
            X-API-Version: 1.0

            {
                "current_render_time": {
                    "$date": 0
                },
                "object_information": {
                    "object_id": 1,
                    "creation_time": {
                      "$date": 0
                    },
                    "last_edit_time": {
                      "$date": 0
                    },
                    "author_id": 1,
                    "author_name": "admin",
                    "editor_id": null,
                    "editor_name": null,
                    "active": true,
                    "version": "1.0.0"
                },
                "type_information": {
                    "type_id": 1,
                    "type_name": "example",
                    "type_label": "Example",
                    "creation_time": {
                      "$date": 0
                },
                "author_id": 1,
                "author_name": "admin",
                "icon": "",
                "active": true,
                "version": "1.0.0",
                "acl": {
                    "activated": false,
                    "groups": {
                        "includes": {}
                    }
                },
                "fields": [
                    {
                        "type": "text",
                        "name": "example",
                        "label": "Example",
                        "value": "value"
                    },
                ],
                "sections": [
                    {
                      "type": "section",
                      "name": "example",
                      "label": "Example-Section",
                      "fields": ["example"]
                    }
                ],
                "summaries": [
                    {
                      "type": "text",
                      "name": "example",
                      "label": "example",
                      "value": "value"
                    }
                ],
                "summary_line": "value",
                "externals": [
                    {
                      "name": "google",
                      "href": "http://www.google.de/value",
                      "label": "Google Search",
                      "icon": "fas fa-external-link",
                      "fields": ["example"]
                    }
                ]
            }

        :reqheader Accept: application/json
        :reqheader Authorization: JW-Token to authenticate
        :resheader Content-Type: application/json
        :statuscode 200: Everything is fine.
        :statuscode 403: No access to this object (For example: ACLs).
        :statuscode 404: No collection or resources found.
        :statuscode 500: Something broke during the rendering.

.. http:get:: /objects/(int:public_id)/native

        Returns an object in its native format. HTTP `GET/HEAD` rest route.
        `HEAD` will be the same result except their will be no body.

        **Example request**:

        .. sourcecode:: http

            GET /rest/objects/1/native HTTP/1.1
            Host: datagerry.com
            Accept: application/json

        **Example response**:

        .. sourcecode:: http

            HTTP/1.1 200 OK
            Content-Type: application/json
            X-Total-Count: 1
            X-API-Version: 1.0

            {
               "public_id": 1,
               "type_id": 1,
               "status": true,
               "version": "1.0.0",
               "creation_time": {
                  "$date": 0
               },
               "author_id": 1,
               "last_edit_time": {
                  "$date": 0
               },
               "editor_id": null,
               "active": true,
               "fields": [
                  {
                     "name": "example",
                     "value": "value"
                  }
               ],
               "views":0
            }

        :reqheader Accept: application/json
        :reqheader Authorization: JW-Token to authenticate
        :resheader Content-Type: application/json
        :statuscode 200: Everything is fine.
        :statuscode 403: No access to this object (For example: ACLs).
        :statuscode 404: No collection or resources found.
        :statuscode 500: Something broke during the rendering.

.. http:get:: /objects/(int:public_id)/references

        HTTP `GET/HEAD` rest route. Returns all objects which reference to the object with the given id.

        **Example request**:

        .. sourcecode:: http

            GET /rest/objects/1/references HTTP/1.1
            Host: datagerry.com
            Accept: application/json

        :query view: Return view of the response. Values `native` or `render`. Default is `native`.
        :query active: Show only active objects. Could also be set over the filter.
        :query sort: the sort field name. default is public_id
        :query order: the sort order value for ascending or descending. Default is 1 for ascending.
        :query page: the current view page. default is 1
        :query limit: max number of results. default is 10
        :query filter: a mongodb query filter. default is {} which means everything
        :query projection: a mongodb project filter.

        :reqheader Accept: application/json
        :reqheader Authorization: JW-Token to authenticate
        :resheader Content-Type: application/json
        :statuscode 200: Everything is fine.
        :statuscode 400: The request or the parameters are wrong formatted.
        :statuscode 403: If the user has no access to the object of this public id.
        :statuscode 404: No collection or resources found.

Create / Update (POST / PUT) - Operation
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

**Validation Schema**

.. code-block::

    {
        'public_id': {
            'type': 'integer'
        },
        'type_id': {
            'type': 'integer'
        },
        'status': {
            'type': 'boolean',
            'required': False,
            'default': True
        },
        'version': {
            'type': 'string',
            'default': DEFAULT_VERSION
        },
        'author_id': {
            'type': 'integer',
            'required': True
        },
        'creation_time': {
            'type': 'dict',
            'nullable': True,
            'required': False
        },
        'last_edit_time': {
            'type': 'dict',
            'nullable': True,
            'required': False
        },
        'active': {
            'type': 'boolean',
            'required': False,
            'default': True
        },
        'fields': {
            'type': 'list',
            'required': True,
            'default': [],
            'schema': {
                'type': 'dict',
                'schema': {
                        "name" : {
                            'type': 'string',
                                'required': true
                        },
                        "value" : {
                            'type': 'string',
                                'nullable': True
                                'required': true
                        },
                }
            }
        }
    }



.. http:post:: /objects/

        HTTP `POST` rest route. Insert a new object.

        **Example request**

        .. sourcecode:: http

            POST /rest/objects/ HTTP/1.1
            Host: datagerry.com
            Accept: application/json
            Content-Type: application/json

            {
                "type_id": 1,
                "version": "1.0.1",
                "author_id": 1,
                "active": true,
                "fields": [
                    {
                        "name" : "dummy-field",
                        "value" : null
                    }
                ],
                "views": 0
            }

        **Example response**

        .. sourcecode:: http

            HTTP/1.1 200 OK
            Content-Type: application/json
            Content-Length: 588
            Location: http://datagerry.com/rest/objects/1
            X-API-Version: 1.0


        :reqheader Accept: application/json
        :reqheader Authorization: JW-Token to authenticate
        :resheader Content-Type: application/json
        :statuscode 200: Everything is fine.
        :statuscode 400: Resource could not be inserted.
        :statuscode 403: No right to insert a new object of this type.
        :statuscode 404: No resource found.
        :statuscode 500: Something went wrong during insertion.

.. http:put:: /objects/(int:public_id)

        HTTP `PUT/PATCH` rest route. Update a existing object.

        **Example request**

        .. sourcecode:: http

            PUT /rest/objects/1 HTTP/1.1
            Host: datagerry.com
            Accept: application/json
            Content-Type: application/json

            {
                "type_id": 1,
                "version": "1.0.1",
                "author_id": 1,
                "active": true,
                "fields": [
                    {
                        "name": "dummy-field",
                        "value": "update"
                    }
                ],
                "public_id": 1,
                "views": 0
            }

        **Example response**

        .. sourcecode:: http

            HTTP/1.1 200 OK
            Content-Type: application/json
            Content-Length: 588
            Location: http://datagerry.com/rest/objects/1
            X-API-Version: 1.0


        :reqheader Accept: application/json
        :reqheader Authorization: JW-Token to authenticate
        :resheader Content-Type: application/json
        :statuscode 200: Everything is fine.
        :statuscode 400: Resource could not be inserted.
        :statuscode 403: No right to update a existing object of this type.
        :statuscode 404: No resource found.
        :statuscode 500: Something went wrong during update.

Delete - Operation
^^^^^^^^^^^^^^^^^^

.. http:delete:: /objects/(int:public_id)

        HTTP `DELETE` rest route. Delete a existing object.

        **Example request**

        .. sourcecode:: http

            DELETE /rest/objects/1 HTTP/1.1
            Host: datagerry.com
            Accept: application/json

        **Example response**

        .. sourcecode:: http

            HTTP/1.1 200 OK
            Content-Type: application/json
            Content-Length: 588
            Location: http://datagerry.com/rest/objects/1
            X-API-Version: 1.0


        :reqheader Accept: application/json
        :reqheader Authorization: JW-Token to authenticate
        :resheader Content-Type: application/json
        :statuscode 200: Everything is fine.
        :statuscode 400: Resource could not be inserted.
        :statuscode 403: No right to delete a object of this type.
        :statuscode 404: No resource found.
        :statuscode 500: Something went wrong during deletion.

.. http:delete:: /objects/(list:public_ids)

        HTTP `DELETE` rest route. Delete multiple existing object.

        **Example request**

        .. sourcecode:: http

            DELETE /rest/objects/1,2,3 HTTP/1.1
            Host: datagerry.com
            Accept: application/json

        **Example response**

        .. sourcecode:: http

            HTTP/1.1 200 OK
            Content-Type: application/json
            Content-Length: 588
            Location: http://datagerry.com/rest/objects/1
            X-API-Version: 1.0


        :reqheader Accept: application/json
        :reqheader Authorization: JW-Token to authenticate
        :resheader Content-Type: application/json
        :statuscode 200: Everything is fine.
        :statuscode 400: Resource could not be inserted.
        :statuscode 403: No right to delete a object of this type.
        :statuscode 404: No resource found.
        :statuscode 500: Something went wrong during deletion.


Special - Operation
^^^^^^^^^^^^^^^^^^^

.. http:get:: /objects/(int:public_id)/state

        HTTP `GET` rest route. Returns the activation state of an object.

        **Example request**:

        .. sourcecode:: http

            GET /rest/objects/1/state HTTP/1.1
            Host: datagerry.com
            Accept: application/json

        :reqheader Accept: application/json
        :reqheader Authorization: JW-Token to authenticate
        :resheader Content-Type: application/json
        :statuscode 200: Everything is fine.
        :statuscode 403: No access to this object (For example: ACLs).
        :statuscode 404: No collection or resources found.

.. http:put:: /objects/(int:public_id)/state

        HTTP `PUT` rest route. Update the activation state of an object.

        **Example request**:

        .. sourcecode:: http

            PUT /rest/objects/1/state HTTP/1.1
            Host: datagerry.com
            Accept: application/json

        :reqheader Accept: application/json
        :reqheader Authorization: JW-Token to authenticate
        :resheader Content-Type: application/json
        :statuscode 200: Everything is fine.
        :statuscode 403: No access to this object (For example: ACLs).
        :statuscode 404: No collection or resources found.

.. http:get:: /objects/clean/(int:public_id)

        HTTP `GET/HEAD` rest route. Returns all unstructured/unclean objects form a type. PublicID is the id of the type.

        **Example request**:

        .. sourcecode:: http

            GET /rest/objects/clean/1 HTTP/1.1
            Host: datagerry.com
            Accept: application/json

        :reqheader Accept: application/json
        :reqheader Authorization: JW-Token to authenticate
        :resheader Content-Type: application/json
        :statuscode 200: Everything is fine.
        :statuscode 403: No access to this object (For example: ACLs).
        :statuscode 404: No collection or resources found.


.. http:put:: /objects/clean/(int:public_id)

        HTTP `PUT` rest route. Cleans all unstructured/unclean objects form a type. PublicID is the id of the type.

        **Example request**:

        .. sourcecode:: http

            PUT /rest/objects/clean/1 HTTP/1.1
            Host: datagerry.com
            Accept: application/json

        :reqheader Accept: application/json
        :reqheader Authorization: JW-Token to authenticate
        :resheader Content-Type: application/json
        :statuscode 200: Everything is fine.
        :statuscode 403: No access to this object (For example: ACLs).
        :statuscode 404: No collection or resources found.

Types
-----
Create and manage your first types via the Rest-API

READ (GET) - Operation
^^^^^^^^^^^^^^^^^^^^^^

Overview of all GET routes to get types from the database.

.. http:get:: /types/

       HTTP GET/HEAD rest route. HEAD will be the same result except their will be no body.

       **Example request**:

       .. sourcecode:: http

          GET /rest/types/ HTTP/1.1
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
                  "active": true,
                  "author_id": 1,
                  "creation_time": "",
                  "label": "Example",
                  "version": "1.0.0",
                  "description": "",
                  "render_meta": {
                    "icon": "",
                    "sections": [
                      {
                        "type": "section",
                        "name": "example",
                        "label": "Example",
                        "fields": [
                          "f"
                        ]
                      }
                    ],
                    "externals": [
                      {
                        "name": "example",
                        "href": "https://example.org",
                        "label": "Example",
                        "icon": "fas fa-external-link-alt",
                        "fields": []
                      }
                    ],
                    "summary": {
                      "fields": [
                        "f"
                      ]
                    }
                  },
                  "fields": [
                    {
                      "type": "text",
                      "name": "f",
                      "label": "F"
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
                "current": "http://datagerry.com/rest/types/",
                "first": "http://datagerry.com/rest/types/?page=1",
                "prev": "http://datagerry.com/rest/types/?page=1",
                "next": "http://datagerry.com/rest/types/?page=1",
                "last": "http://datagerry.com/rest/types/?page=1"
              },
              "response_type": "GET",
              "model": "Type",
              "time": "1970-01-01T00:00:00"
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

.. http:get:: /types/(int:public_id)

        HTTP GET/HEAD rest route for a single resource by its ID.

        **Example request**

        .. sourcecode:: http

            GET /rest/types/1 HTTP/1.1
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
                  "active": true,
                  "author_id": 1,
                  "creation_time": "",
                  "label": "Example",
                  "version": "1.0.0",
                  "description": "",
                  "render_meta": {
                    "icon": "",
                    "sections": [
                      {
                        "type": "section",
                        "name": "example",
                        "label": "Example",
                        "fields": [
                          "f"
                        ]
                      }
                    ],
                    "externals": [
                      {
                        "name": "example",
                        "href": "https://example.org",
                        "label": "Example",
                        "icon": "fas fa-external-link-alt",
                        "fields": []
                      }
                    ],
                    "summary": {
                      "fields": [
                        "f"
                      ]
                    }
                  },
                  "fields": [
                    {
                      "type": "text",
                      "name": "f",
                      "label": "F"
                    }
                  ]
                },
                "response_type": "GET",
                "model": "Type",
                "time": "1970-01-01T00:00:00"
            }

        :reqheader Accept: application/json
        :reqheader Authorization: jwtoken to authenticate
        :resheader Content-Type: application/json
        :statuscode 200: Everything is fine.
        :statuscode 404: No resource found.

Create / Update (POST / PUT) - Operation
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

**Validation Schema**

.. code-block::

    {
        'public_id': {
            'type': 'integer'
        },
        'name': {
            'type': 'string',
            'required': True,
            'regex': r'(\w+)-*(\w)([\w-]*)'  # kebab case validation,
        },
        'label': {
            'type': 'string',
            'required': False
        },
        'author_id': {
            'type': 'integer',
            'required': True
        },
        'editor_id': {
            'type': 'integer',
            'nullable': True,
            'required': False
        },
        'active': {
            'type': 'boolean',
            'required': False,
            'default': True
        },
        'fields': {
            'type': 'list',
            'required': False,
            'default': None,
            'schema': {
                'type': 'dict',
                'schema': {
                    "type": {
                        'type': 'string',  # Text, Password, Textarea, radio, select, date
                        'required': True
                    },
                    "required": {
                        'type': 'boolean',
                        'required': False
                    },
                    "name": {
                        'type': 'string',
                        'required': True
                    },
                    "label": {
                        'type': 'string',
                        'required': True
                    },
                    "description": {
                        'type': 'string',
                        'required': False,
                    },
                    "regex": {
                        'type': 'string',
                        'required': False
                    },
                    "placeholder": {
                        'type': 'string',
                        'required': False,
                    },
                    "value": {
                        'type': 'string',
                        'required': False,
                    },
                    "helperText": {
                        'type': 'string',
                        'required': False,
                    },
                    "default": {
                        'type': 'integer',
                        'nullable': True,
                        'empty': True
                    },
                    "options": {
                        'type': 'list',
                        'empty': True,
                        'required': False,
                        'schema': {
                            'type': 'dict',
                            'schema': {
                                "name": {
                                    'type': 'string',
                                    'required': True
                                },
                                "label": {
                                    'type': 'string',
                                    'required': True
                                },
                            }
                        }
                    },
                    "ref_types": {
                        'type': 'list',  # List of public_id of type
                        'required': False,
                        'empty': True,
                        'schema': {
                            'type': 'integer',
                        }
                    },
                    "summaries": {
                        'type': 'list',
                        'empty': True,
                        'schema': {
                            'type': 'dict',
                            'schema': {
                                "type_id": {
                                    'type': 'integer',
                                    'required': True
                                },
                                "line": {
                                    'type': 'string',
                                    # enter curved brackets for field interpolation example: Customer IP {}
                                    'required': True
                                },
                                "label": {
                                    'type': 'string',
                                    'required': True
                                },
                                "fields": {  # List of field names
                                    'type': 'list',
                                    'empty': True,
                                    'schema': {
                                        'type': 'string',
                                        'required': False
                                    },
                                },
                                "icon": {
                                    'type': 'string',  # Free Font Awesome example: 'fa fa-cube'
                                    'required': True
                                },
                                "prefix": {
                                    'type': 'boolean',
                                    'required': False,
                                    'default': True
                                }
                            }
                        }
                    }
                }
            },
        },
        'version': {
            'type': 'string',
            'default': DEFAULT_VERSION
        },
        'description': {
            'type': 'string',
            'nullable': True,
            'empty': True
        },
        'render_meta': {
            'type': 'dict',
            'allow_unknown': False,
            'schema': {
                'icon': {
                    'type': 'string',
                    'nullable': True
                },
                'sections': {
                    'type': 'list',
                    'schema': {
                        'type': 'dict',
                        'schema': {
                            "type": {
                                'type': 'string',
                                'required': True
                            },
                            "name": {
                                'type': 'string',
                                'required': True
                            },
                            "label": {
                                'type': 'string',
                                'required': True
                            },
                            "reference": {
                                'type': 'dict',
                                'empty': True,
                                'schema': {
                                    "type_id": {
                                        'type': 'integer',
                                        'required': True
                                    },
                                    "section_name": {
                                        'type': 'string',
                                        'required': True
                                    },
                                    'selected_fields': {
                                        'type': 'list',
                                        'empty': True
                                    }
                                }
                            },
                            'fields': {
                                'type': 'list',
                                'schema': {
                                    'type': 'string',
                                    'required': False
                                },
                                'empty': True,
                            }
                        }
                    },
                    'empty': True
                },
                'externals': {
                    'type': 'list',
                    'schema': {
                        'type': 'dict',
                        'schema': {
                            'name': {
                                'type': 'string',
                                'required': True
                            },
                            'href': {
                                'type': 'string',  # enter curved brackets for field interpolation example: Field {}
                                'required': True
                            },
                            'label': {
                                'type': 'string',
                                'required': True
                            },
                            'icon': {
                                'type': 'string',
                                'required': True
                            },
                            'fields': {
                                'type': 'list',
                                'schema': {
                                    'type': 'string',
                                    'required': False
                                },
                                'empty': True,
                            }
                        }
                    },
                    'empty': True,
                },
                'summary': {
                    'type': 'dict',
                    'schema': {
                        'fields': {
                            'type': 'list',
                            'schema': {
                                'type': 'string',
                                'required': False
                            },
                            'empty': True,
                        }
                    },
                    'empty': True
                }
            }
        },
        'acl': {
            'type': 'dict',
            'allow_unknown': True,
            'required': False,
        }
    }

.. http:post:: /types/

        HTTP Post route for inserting a new type.

        **Example request**

        .. sourcecode:: http

            POST /rest/types/ HTTP/1.1
            Host: datagerry.com
            Content-Type: application/json
            Accept: application/json

            {
                "name" : "dummy-type-example",
                "label" : "Example Type",
                "description" : "",
                "version" : "1.0.0",
                "status" : null,
                "active" : true,
                "clean_db" : true,
                "access" : {
                    "groups" : "",
                    "users" : ""
                },
                "author_id" : 1,
                "render_meta" : {
                    "icon" : "fab fa-windows",
                    "sections" : [
                        {
                            "type" : "section",
                            "name" : "basic-sections",
                            "label" : "Basicsection",
                            "fields" : [
                                "dummy-field"
                            ]
                        }
                    ],
                    "externals" : [],
                    "summary" : {
                        "fields" : [
                            "dummy-field"
                        ]
                    }
                },
                "fields" : [
                    {
                        "type" : "text",
                        "name" : "dummy-field",
                        "label" : "Label may differ"
                    }

                ],
                "category_id" : null,
                "acl" : {
                    "activated" : false,
                    "groups" : {
                        "includes" : {}
                    }
                }
            }

        **Example response**

        .. sourcecode:: http

            HTTP/1.1 200 OK
            Content-Type: application/json
            Content-Length: 588
            Location: http://datagerry.com/rest/types/1
            X-API-Version: 1.0

            {
              "result_id": 1,
              "raw": {},
              "response_type": "INSERT",
              "model": "Type",
              "time": "1970-01-01T00:00:00"
            }

        :reqheader Accept: application/json
        :reqheader Authorization: jwtoken to authenticate
        :resheader Content-Type: application/json
        :statuscode 200: Everything is fine.
        :statuscode 400: Resource could not be inserted.
        :statuscode 404: No resource found.

.. http:put:: /types/(int:public_id)

        HTTP `PUT`/`PATCH` route for updating a existing type.

        **Example request**

        .. sourcecode:: http

            PUT /rest/types/1 HTTP/1.1
            Host: datagerry.com
            Content-Type: application/json
            Accept: application/json

            {
                "name" : "dummy-type-example",
                "label" : "Example Type",
                "description" : "",
                "version" : "1.0.0",
                "status" : null,
                "active" : true,
                "clean_db" : true,
                "public_id": 1,
                "access" : {
                    "groups" : "",
                    "users" : ""
                },
                "author_id" : 1,
                "render_meta" : {
                    "icon" : "fab fa-windows",
                    "sections" : [
                        {
                            "type" : "section",
                            "name" : "basic-sections",
                            "label" : "Basicsection",
                            "fields" : [
                                "dummy-field"
                            ]
                        }
                    ],
                    "externals" : [],
                    "summary" : {
                        "fields" : [
                            "dummy-field"
                        ]
                    }
                },
                "fields" : [
                    {
                        "type" : "text",
                        "name" : "dummy-field",
                        "label" : "Rename field label"
                    }

                ],
                "category_id" : null,
                "acl" : {
                    "activated" : false,
                    "groups" : {
                        "includes" : {}
                    }
                }
            }

        **Example response**

        .. sourcecode:: http

            HTTP/1.1 202 ACCEPTED
            Content-Type: application/json
            Content-Length: 170
            Location: http://datagerry.com/rest/categories/1
            X-API-Version: 1.0

            {
              "result": {
              },
              "response_type": "UPDATE",
              "model": "Type",
              "time": "1970-01-01T00:00:00"
            }

        :reqheader Accept: application/json
        :reqheader Authorization: jwtoken to authenticate
        :resheader Content-Type: application/json
        :statuscode 202: Everything is fine.
        :statuscode 400: Resource could not be updated.
        :statuscode 404: No resource found.

Delete - Operation
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. http:delete:: /type/(int:public_id)

        HTTP `DELETE` route for deleting a existing type.

        **Example request**

        .. sourcecode:: http

            DELETE /rest/types/1 HTTP/1.1
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
              },
              "response_type": "DELETE",
              "model": "Type",
              "time": "1970-01-01T00:00:00"
            }

        :reqheader Accept: application/json
        :reqheader Authorization: jwtoken to authenticate
        :resheader Content-Type: application/json
        :statuscode 202: Everything is fine.
        :statuscode 400: Resource could not be deleted.
        :statuscode 404: No resource found.

Categories
----------

Create and manage your first categories via the Rest-API

READ (GET) - Operation
^^^^^^^^^^^^^^^^^^^^^^

Overview of all GET routes to get categories from the database.

.. http:get:: /categories/

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
                "current": "http://datagerry.com/rest/categories/",
                "first": "http://datagerry.com/rest/categories/?page=1",
                "prev": "http://datagerry.com0/rest/categories/?page=1",
                "next": "http://datagerry.com/rest/categories/?page=1",
                "last": "http://datagerry.com/rest/categories/?page=1"
              },
              "response_type": "GET",
              "model": "Category",
              "time": "1970-01-01T00:00:00"
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

.. http:get:: /categories/(int:public_id)

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
              "time": "1970-01-01T00:00:00"
            }

        :reqheader Accept: application/json
        :reqheader Authorization: jwtoken to authenticate
        :resheader Content-Type: application/json
        :statuscode 200: Everything is fine.
        :statuscode 404: No resource found.

Create / Update (POST / PUT) - Operation
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

**Validation Schema**

.. code-block::
        {
            'public_id': {
                'type': 'integer'
            },
            'name': {
                'type': 'string',
                'required': True,
                'regex': r'(\w+)-*(\w)([\w-]*)'  # kebab case validation,
            },
            'label': {
                'type': 'string',
                'required': False
            },
            'parent': {
                'type': 'integer',
                'nullable': True,
                'default': None
            },
            'types': {
                'type': 'list',	# List of public_id of Types
                'default': []
            },
            'meta': {
                'type': 'dict',
                'schema': {
                    'icon': {
                        'type': 'string',
                        'empty': True
                    },
                    'order': {
                        'type': 'integer',
                        'nullable': True
                    }
                },
                'default': {
                    'icon': '',
                    'order': None,
                }
            }
        }


.. http:post:: /categories/

        HTTP Post route for inserting a new category.

        **Example request**

        .. sourcecode:: http

            POST /rest/categories/ HTTP/1.1
            Host: datagerry.com
            Content-Type: application/json
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
            Location: http://datagerry.com/rest/categories/1
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
              "time": "1970-01-01T00:00:00"
            }

        :reqheader Accept: application/json
        :reqheader Authorization: jwtoken to authenticate
        :resheader Content-Type: application/json
        :statuscode 200: Everything is fine.
        :statuscode 400: Resource could not be inserted.
        :statuscode 404: No resource found.

.. http:put:: /categories/(int:public_id)

        HTTP `PUT`/`PATCH` route for updating a existing category.

        **Example request**

        .. sourcecode:: http

            PUT /rest/categories/1 HTTP/1.1
            Host: datagerry.com
            Content-Type: application/json
            Accept: application/json

            {
              "public_id": 1,
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
            Location: http://datagerry.com/rest/categories/1

            {
              "result": {
                "public_id": 1,
                "name": "example2",
                "label": "Example",
                "meta": {
                  "icon": "",
                  "order": 0
                },
                "parent": null,
                "types": []
              },
              "response_type": "UPDATE",
              "model": "Category",
              "time": "1970-01-01T00:00:00"
            }

        :reqheader Accept: application/json
        :reqheader Authorization: jwtoken to authenticate
        :resheader Content-Type: application/json
        :statuscode 202: Everything is fine.
        :statuscode 400: Resource could not be updated.
        :statuscode 404: No resource found.

.. http:delete:: /categories/(int:public_id)

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
              "time": "1970-01-01T00:00:00"
            }

        :reqheader Accept: application/json
        :reqheader Authorization: jwtoken to authenticate
        :resheader Content-Type: application/json
        :statuscode 202: Everything is fine.
        :statuscode 400: Resource could not be deleted.
        :statuscode 404: No resource found.