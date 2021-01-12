import setuptools
from distutils.command.build_py import build_py

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="yalafi",
    version="1.2.0",
    author="Matthias Baumann",
    description="Yet another LaTeX filter",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/matze-dd/YaLafi",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
        "Operating System :: OS Independent",
        "Topic :: Text Processing :: Markup :: LaTeX",
        "Topic :: Text Processing :: Filters",
    ],
    cmdclass = {"build_py": build_py},
    entry_points = {
        "console_scripts": [
            "yalafi = yalafi.shell.__main__:main",
        ]
    }
)
