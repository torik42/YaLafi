# Contributing to YaLafi

Any contributions are welcome!
If you encounter any problem or missing LaTeX command feel free to open an issue on [GitHub](https://github.com/torik42/YaLafi/issues).
If you want to add the command yourself, the following guide might be helpful.
Feel free to open pull requests, even if some steps are still missing.

## Installation for development

If you want to develop YaLafi, you might want to create a second environment using your favourite environment manager.
Then clone the repository and run (from within the repository)
```
pip install --editable .
```
to install YaLafi in [editable mode](https://pip.pypa.io/en/stable/topics/local-project-installs/#editable-installs).
If you see an error about a missing `setup.py`, you need to update pip (more recent versions have support for editable installs using `pyproject.toml`).

## Run tests locally
To run the test suit locally, first navigate to the repository and then execute:
```
python -m pytest
```
Individual tests can be run using (for example):
```
python -m pytest tests/test_packages/test_latex_builtins.py
```
The tests are run using the currently installed version of YaLafi.
It is therefore recommended installing YaLafi in [editable mode](#installation-for-development) if you want to develop YaLafi.
Then the above commands will use the source files.
Otherwise you would need to reinstall YaLafi before you execute the tests again.

In case you only added or changed LaTeX commands, you can ignore errors in `test_shell/…` and `test_shell_cmd/…` which depend on the environment.
In particular, the test suit has its own imitation of a LanguageTool server which uses the default port.
Hence, you need to shut down any locally running (LanguageTool) servers on port 8081 to make these tests pass.


## Add more LaTeX commands
To add support for additional LaTeX macros, first have a look at [inclusion of own macros](README.md#inclusion-of-own-macros).
Then decide where the command or the extra functionality you want to add stems from.
Default LaTeX commands are in [yalafi/parameters.py](yalafi/parameters.py). In there you find a list of LaTeX commands, lists of macro and environment definitions and some more special tokens.
If the command (or a variant with more options) stems from a package or document class, please add them to `yalafi/packages/<package_name>.py` or `yalafi/packages/<documentclass_name>.py`.
In case the package does not exist yet, have a look at the [next section](#additional-latex-package).

After you added the LaTeX commands, please also add tests in `tests/…`.
The names of the files and commands already tested there should help you find the right file.
Everything related to packages or document classes is in `tests/test_packages/test_<package_name>.py`.
Most tests for plain LaTeX commands are in `tests/test_packages/test_latex_builtins.py`.
More specific custom tests (which you usually don’t need to change) are in `tests`, `tests/test_issues`, `test_shell` and `test_shell_cmd`.

How to run tests locally is described in [Run tests locally](#run-tests-locally).
And they will also be run online when you open a pull request.

The tests are important because they often show shortcomings of an implementation and help to find a better one.
It is particular important to include tests for things you wouldn’t find in a correct document so that we don’t miss any spelling mistakes later on.
To always find white space errors, we often include some extra surrounding letters, see the following examples for `\hspace` from `tests_test_packages/test_latex_builtins.py` (running the YaLafi parser on the first entry of each tuple should evaluate to the second entry)
```
    (r'A\hspace{1em}B', 'A B'),
    (r'A\hspace*{1em}B', 'A B'),
    (r'A\hspace{0cm}B', 'AB'),
    (r'A\hspace{ .0cm}B', 'AB'),
```

Even without tests, feel free to open a PR, and we can add them later on.

Finally, please add all new commands to `list-of-macros.md`.


## Add a new LaTeX package or document class
If you want to add support for an additional LaTeX package then the following
might be helpful.

Each LaTeX package corresponds to a Python module in directory
[yalafi/packages](yalafi/packages).
You can find relevant information on interfaces in sections
[Extension modules for LaTeX packages](README.md#extension-modules-for-latex-packages)
and
[Inclusion of own macros](README.md#inclusion-of-own-macros)
of [README.md](README.md).

A basic example is [amsmath.py](yalafi/packages/amsmath.py),
more techniques are demonstrated in
[cleveref.py](yalafi/packages/cleveref.py),
[glossaries.py](yalafi/packages/glossaries.py), and
[xspace.py](yalafi/packages/xspace.py).
Unfortunately, a complete documentation of the internal interfaces does not
exist, yet.

Here is a summary of the necessary steps:

- Add a file `yalafi/packages/package_name.py` implementing all the needed
  commands of the package.
- Add a file `yalafi/tests/test_packages/test_package_name.py` testing all the
  features.
- Add the package and implemented features to `list-of-macros.md` and
  reference it in the Contents section.
- Add the package to the default package list in `yalafi/packages/__init__.py`.

Adding a new LaTeX document class goes along similar lines.

## Coding conventions

Please use indentation shifts of 4 characters and at most 79 characters per line.