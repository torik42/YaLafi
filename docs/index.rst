.. YaLafi documentation master file, created by
   sphinx-quickstart on Sat Mar 18 16:18:47 2023.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

YaLafi: Yet another LaTeX filter
================================

`YaLafi` is a Python package to extract plain text from LaTeX documents for proofreading.
The subpackage ``yalafi.shell`` integrates YaLafi with the proofreading software `LanguageTool <https://languagetool.org>`_.

.. warning::
   This is the new documentation for YaLafi.
   If you cannot find something here, please also look into the old documentation in the `README <https://github.com/torik42/YaLafi#readme>`_ and in `list-of-macros.md <https://github.com/torik42/YaLafi/blob/master/list-of-macros.md>`_.
   We also keep everything not yet merged to the new documentation in :doc:`remaining-old-documentation`.

.. toctree::
   :maxdepth: 2
   :caption: Getting started

   installation
   basic-usage
   editor-integration


.. toctree::
   :maxdepth: 2
   :caption: Documentation

   yalafi-interfaces
   remaining-old-documentation


API Reference
-------------

If you know what you are looking for, here is our automatically generated API
documentation.

.. toctree::
   :maxdepth: 1
   :caption: API Reference
   :hidden:

   auto-api/yalafi
   auto-api/yalafi.shell
   auto-api/yalafi.documentclasses
   auto-api/yalafi.packages


* :doc:`auto-api/yalafi`
* :doc:`auto-api/yalafi.shell`
* :doc:`auto-api/yalafi.documentclasses`
* :doc:`auto-api/yalafi.packages`
