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


latest symlink
--------------

A *latest* symlink should be set to the latest stable version of DATAGERRY. At the moment, we have to do that manually
after the CI process was done. Maybe we'll autmate that in the future.

The symlink needs to be set on:

 * files.datagerry.com
 * docs.datagerry.com
 * Docker hub

To set the latest tag for our Docker image on Docker Hub, the image for the release needs to be downloaded, retagged and
uploaded agaign.

.. code-block:: console

    docker pull nethinks/datagerry:1.0.2
    docker tag nethinks/datagerry:1.0.2 nethinks/datagerry
    docker push nethinks/datagerry:latest
