.. _contributing_to_the_docs:

=========================
Contributing to the docs
=========================

This section intend to give developers a few guidelines on how to write the
documentation.


Setting up Sphinx for productive documentation
==============================================
Starting with installing the ``doc`` requirements.

1. Install the requirements for the docs by running:

.. code-block:: bash

  pip install meteofrance_publicapi[doc]


Building the documentation
==========================
From the root directory, run the command  :

.. code-block:: bash

  sphinx-build -M html ./doc ./build/sphinx

This command will parse the ``./doc/``  folder content and generate html files from it in the folder ``./build/sphinx/html``

Going further with rST
==========================
Useful information about the rST markup :

-  `rST-Cheatsheet <https://github.com/ralsina/rst-cheatsheet/blob/master/rst-cheatsheet.rst>`_
-  `Sphinx rST doc page <https://www.sphinx-doc.org/en/master/usage/restructuredtext/index.html>`_


The 4 types of documents
==========================

There is a summary of  `the documentation system <https://documentation.divio.com/>`_ .

There is a secret that needs to be understood in order to write good software
documentation: there isn't one thing called documentation, there are four :

1. **tutorials** : aimed to teach new users the main principles
2. **how-to guides** : aimed to provide simple answers to recurring questions
3. **technical reference** : aimed to describe the code, and how to operate it
4. **explanation** : aimed to clarify and illuminate a particular topic.

.. image:: /_static/overview_4types_of_docs.png
   :width: 600


**The Secrets of each type**

.. list-table::  **The main ideas for the 4 kind of docs**
   :widths: 25 25 25 25 25
   :header-rows: 1

   * -
     - Tutorials
     - How-Tos
     - Technical Reference
     - Explanation
   * - *Oriented to*
     - learning
     - a goal
     - information
     - understanding
   * - *Must*
     - allow the newcomer to get started
     - show how to solve a specific problem
     - describe the machinery
     - explain
   * - *Its form*
     - a lesson
     - a series of steps
     - dry description
     - discursive explanation
   * - *Analogy*
     - teaching a small child how to cook
     - a recipe in a cookery book
     - a reference encyclopedia article
     - an article on culinary social history


Using Docstring
=================
Docstring is an important part of documentation : by keeping the documentation
close to the code, it unsure that:

- it can be easily updated with the function code;
- it can be used in IDE for auto-completion, type hints and such.

Including Math
###############
Equations can easily be included in the doc, both inline
``:math:\frac{ \sum_{t=0}^{N}f(t,k) }{N}`` (that renders as
:math:`\frac{ \sum_{t=0}^{N}f(t,k) }{N}`) and as a block

.. code-block::

  .. math::

   \frac{ \sum_{t=0}^{N}f(t,k) }{N}

that renders as :

.. math::

   \frac{ \sum_{t=0}^{N}f(t,k) }{N}

Including code block
####################
To illustrate the use of a function, it can be interesting to add a code-block
following this syntax :

.. code-block:: text

  .. code-block:: python

    value = myfunction(arg1, arg2)
    print(value)

that renders as:

.. code-block:: python

  value = myfunction(arg1, arg2)
  print(value)

(you see the syntax highlighting?)

Generating new pages for new modules
=====================================
When a new module is added to the code, it is important to add a new page in the documentation.

To do so, the new file must:
- be created in the ``./doc/source/`` folder
- be named after the module name (e.g. ``my_module.rst``)
- be referenced in a doctree (usually the parent module)

You can do the first two steps easily using ``sphinx-apidoc`` :
.. code-block:: bash

  sphinx-apidoc -MP -e -o doc/sources meteofrance_publicapi
