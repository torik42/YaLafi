Installation
------------

To use YaLafi for proofreading, you need to install YaLafi and LanguageTool.

Installing YaLafi
^^^^^^^^^^^^^^^^^

.. highlight:: console

To install the YaLafi python package, choose one of the following options.

* To install the latest version from `PyPI <https://www.pypi.org>`_, use::

      python -m pip install yalafi

* To install the current snapshot from the GitHub Repository, use::

      python -m pip install git+https://github.com/torik42/YaLafi.git@master

* For developing YaLafi, editable installation is recommended. See `Contributing.md <https://github.com/torik42/YaLafi/blob/master/CONTRIBUTING.md>`_ for details.


Installing LanguageTool
^^^^^^^^^^^^^^^^^^^^^^^

Although you can use the LanguageTool online service, it is recommended to install LanguageTool on your machine.
Choose one of the following options.

* On most systems, you have to install it manually: First download the
  LanguageTool zip archive, for example ``LanguageTool-5.0.zip``, from
  `LanguageTool download page <https://www.languagetool.org/download>`_ and
  uncompress it at a suitable place. The directory should contain the file
  ``languagetool-server.jar``. To use ``yalafi.shell`` you pass this directory with
  option  ``--lt-directory``.

  .. warning::
      Please note that the new LanguageTool Applications for `Windows <https://languagetool.org/windows>`_ and `macOS <https://languagetool.org/mac>`_ will *not* work, you need to download the above-mentioned zip archive.

* On some distributions you can also use a package manager. Under Arch Linux,
  you can simply say ``sudo pacman -S languagetool``. When using ``yalafi.shell``
  you then need to specify ``--lt-command languagetool``.

  .. warning::
      Please note that, for example under Ubuntu,
      ``sudo snap install languagetool`` will *not* install the components required here.

* If you already have a local LanguageTool server running, you don’t
  need to install anything. When using ``yalafi.shell`` you just pass
  ``--server my`` (see :ref:`basic_usage_command_line` for more details).