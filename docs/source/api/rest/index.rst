.. _rest:

###############################
Representational State Transfer
###############################

To communicate with DATAGERRY a REST interface is provided.
This is subdivided into the areas ``data management`` and ``configuration``.

***************
Allowed methods
***************
HTTP defines a set of request methods to indicate the desired action to be performed for a given resource.
Although they can also be nouns, these request methods are sometimes referred as HTTP verbs.

1. ``GET`` - Requests using `GET` should only retrieve data.
2. ``POST`` - The `POST` method is used to submit new data to the specified resource
3. ``PUT`` - The `PUT` method updates all current data of the target resource with the request payload.
4. ``DELETE`` - The `DELETE` method deletes the specified data.

*******************
Permalink structure
*******************
The permalinks serve as a unique identification of a certain method to a URL.
This structure should be maintained when creating new routes. In principle, the structure of the modules is
always applied. This means that only the basic routes provide all data.
If specific selections are made, these are defined in the subroutes.
If possible, parameterization should be avoided.

.. note::
    This routes should always work with and without ending slash!

1. GET
======
.. csv-table:: permalink get table
    :file: fixtures/permalink_get_table.csv
    :header-rows: 1
    :stub-columns: 1
    :align: left

2. POST
=======
.. csv-table:: permalink post table
    :file: fixtures/permalink_post_table.csv
    :header-rows: 1
    :stub-columns: 1
    :align: left

3. PUT
======
.. csv-table:: permalink put table
    :file: fixtures/permalink_put_table.csv
    :header-rows: 1
    :stub-columns: 1
    :align: left

4. DELETE
=========
.. csv-table:: permalink delete table
    :file: fixtures/permalink_delete_table.csv
    :header-rows: 1
    :stub-columns: 1
    :align: left

******
Routes
******

