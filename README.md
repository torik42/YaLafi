
# YaLafi: Yet another LaTeX filter

This is work in progress, related to
[Tex2txt](https://github.com/matze-dd/Tex2txt).

The aim is to develop a solution with
- a simple tokeniser for the LaTeX input and
- a small machinery for macro expansion.

First examples can be seen in directory tests/.
File tex2txt.py provides an interface between Tex2txt and
YaLafi, such that the application script Tex2txt/shell.py
can be run unmodified.
