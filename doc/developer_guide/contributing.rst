.. _contributing_to_udwi_connector_landing_page:

Developer Guide
===============

This part of the documentation is a comprehensive resource for contributing to
udwi_connector - for both new and experienced contributors.

We welcome your contributions to udwi_connector!

Intended audience
=================
This guide is intended primarily for developers who want to work on udwi_connector,
or its documentation.
It provides information on how to install it, how to test it, and how to contribute.


Testing udwi_connector
======================
Testing is a mandatory step in the process of contributing to the project.
As a mater of fact, it should be considered as the fest step after installing udwi_connector.

Please refer to the :ref:`testing` page for more information about the tests.

Branch management and CI/CD
===========================
The specificities of the branches and the deployments are describes in :ref:`branches_and_CD`

Contributing to the docs
========================
Every contribution should be documented. If you are new to documenting a python
project using ``sphinx``, you can refer to the :ref:`contributing_to_the_docs`
page.

Contributing to the code base
=============================

Now that both Tests and Documentations has been covered, we can discuss on
actually contributing to ``meteofrance_publicapi``.

Quick reference : How-to Contribute
-----------------------------------
Here are the basic steps needed to get set up and contribute a patch.
This is meant as a checklist, once you know the basics.
For complete instructions please see the setup guide.

1.  Get the source code using ``git`` and install it

    .. code-block:: bash

        git clone https://github.com/antoinetavant/meteofranceapi.git
        cd meteofranceapi
        pip install -e .[all]

    The option ``-e`` is used for an "editable installation".
    You can change the code of ``meteofrance_publicapi`` and test it without requiring to install it again.
2.  Test the installation (for details see :doc:`running the tests <testing>` )

    .. code-block:: bash

        python3 -c "from meteofrance_publicapi.tests.main import run; run()"

3.  Create a new branch where your work for the issue will go.
    The branch name must start with the issue number, and a short description of the issue.
    If an issue does not already exist, please create it.

4. Once you fixed the issue, run the tests as in step 2.
5. Update the documentation
6. Push the branch and create a Pull Request. Include the issue to
   close in the descriptions like that : ``Closes #12345``

.. toctree::
    :hidden:
    :maxdepth: 1
    :caption: Developer guide

    contributing_to_docs
    branches_and_CD
    testing
