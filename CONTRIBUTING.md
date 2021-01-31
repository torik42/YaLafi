
# Contributing to YaLafi

Any contributions are welcome!
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

Please use indentation steps of 4 characters and at most 79 characters per
line.

Here is a summary of the necessary steps, courtesy of @torik42
(issue [#167](../../issues/167)).

- Add a file `yalafi/packages/package_name.py` implementing all the needed
  commands of the package.
- Add a file `yalafi/tests/test_packages/test_package_name.py` testing all the
  features.
- Add the package and implemented features to `list-of-macros.md` and
  reference it in the Contents section.
- Add the package to the default package list in `yalafi/packages/__init__.py`.

Adding a new LaTeX document class goes along similar lines.

