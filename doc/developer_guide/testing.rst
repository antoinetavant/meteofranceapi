.. _testing:

Testing
=======


Running the tests
=================

.. warning::

  The test uses requests to the API. An application key is required to run the tests.

To run the tests, the preferred way is to us the following command:

.. code-block:: bash

  python3 -c "from meteofrance_publicapi.tests.main import run; run()"

This method is preferred than running ``pytest ./tests``, in the sources,
which run the tests in the current source directory and not the installation.

When using a function as done here, you ensure the following :

- the tests are run in the installed code base,
- the version of the code you're testing is the one which is used by python in
  your target environment, where the code is installed.

Reformulating, it is one way of satisfying the following requirements :

- only the installed code is tested,
- the tested code is the one that "you're using right now in your current environment".

Running the tests for a developer
=================================

While developing, when iterating quickly on the code base, an alternative way is to :

1. Install ``meteofrance_publicapi`` using the *editable* mode :
    ``pip install -e .[test]``

2.   Run the test as in production with the command above
3.   Contributing to the tests

As testing in the dev. environment is a discouraged practice, prefer applying
the advice above in your testing environment, at least when your code base
becomes more stable.

Updating or creating new tests
==============================

The tests of ``meteofrance_publicapi`` use the ``pytest`` package. Please refer to
`its documentation`_  to learn how to use it.

There are several types of tests denominations:

- unit tests: that tests exhaustively one function (taking care of edge-cases)
- integration tests: that verify that a part of the code is working as expected.
- Validation tests: test all the code base on a full case
- back-reproducibility tests: sometime, it is useful to make sure that we obtain the same results.

Make sure to implement at least the unit tests of your contribution.
See :doc:`meteofrance_publicapi.tests </sources/meteofrance_publicapi.tests>` to get a feeling on how the library
tests are currently implemented.

A few guidelines about how to write the tests are still located `on the wiki`_.

.. _its documentation: https://docs.pytest.org/en/7.1.x/getting-started.html
