.. _branches_and_CD:

Branch management and CI/CD
===========================

Branches
^^^^^^^^

There is no specific branch management for this project for now !

Good practices are:
- use the ``main`` branch as the stable branch used for releases
- when contributing, create a branch from the ``main`` branch and create a pull request to merge it back to the ``main`` branch
- the new branch should be named after the issue number (e.g. ``issue_1-short_description``)

Continuous Deployment
^^^^^^^^^^^^^^^^^^^^^^

The deployment of the package is done at each GitHub release on the ``main`` branch.
The package is then uploaded to the package repository on pypi.org.

Continuous integration
^^^^^^^^^^^^^^^^^^^^^^

The CI is done on each push.

Package Version and releases
^^^^^^^^^^^^^^^^^^^^^^^^^^^^

The package version is defined in the ``__init__.py`` file and must be updated at each release.
