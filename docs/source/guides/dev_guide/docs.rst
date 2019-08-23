*************
Documentation
*************

The Datagerry documentation is created using Sphinx.


Generation
==========
In the case of a push or merge into one of the productive or development branches,
the documentation is automatically generated via our continuous integration.
Depending on the publication method, the documentation is then available
as HTML source under ``/docs/_build/``. Alternatively, the documentation can also be
created manually using the included make file.

Approach
========
Since the documentation consists of pure HTML, it can be accessed directly via the index.html
in the directory ``/docs/_build`` in a browser. Alternatively, the documentation is delivered for
every running instance at https://yourdomain.com/**docs**/ .