import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="yalafi",
    version="1.1.1",
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
)
