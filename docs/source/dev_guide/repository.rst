**************
GIT Repository
**************

The source code of DATAGERRY is managed in a GIT repository on GitHub:

    https://github.com/NETHINKS/DATAGERRY


Branches
========
We use several branches in our GIT repository:

development
    The development of DATAGERRY is done in this branch. Every new feature, bugfix, ... should be commited to that
    branch.

master
    Branch with a stable version of DATAGERRY. All integration tests and CircleCI should have been passed before merging
    the development branch into master. A merge of development to master will usually be done at the end of a sprint.

version-<version>
    Version branches should be created for every minor version, e.g. version-1.2 or version-1.5. It should branch from
    master. For each released version (e.g. 1.2.1), a tag should be set on a version branch. Bugfixes can be added to a
    version branch to prepare for a new bugfix release (e.g. 1.2.2)


Creating a Release
==================

Releases should be versioned using `Semantic Versioning <https://semver.org>`_.

To create a release, do the following steps:

1. create a version-<minorversion> (e.g. version-1.2) branch from master
2. set a tag with the full version number (e.g. 1.2.1) on the last commit on that branch

To create a bugfix release of an existing version, do the following steps:

1. merge bugfixes in an exitsing version-<minorversion> branch
2. set a tag with the full version number (e.g. 1.2.1) on the last commit on that branch

A tag should be set by creating a release in the GitHub WebUI. CircleCI will start automatically after setting a new 
tag and will create binaries, Docker images and documentation. Add the built tar.gz and binary to the GitHub release.


.. note::
    On our two plattforms files.datagerry.com and docs.datagerry.com, the latest symlink should be set to new tag.
