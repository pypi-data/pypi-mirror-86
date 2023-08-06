MatJax for Sphinx Offline
=========================

This provides the Mathjax files for Sphinx without having to rely on an external CDN.

Installation
------------

MathJax for Sphinx Offline is published on `PyPI`__ and can be installed from there::

   pip install -U sphinx-mathjax-offline


In Sphinx ``conf.py``, add ``sphinx.ext.mathjax`` and ``sphinx-mathjax-offline`` to ``extensions``.
This will then automatically set ``mathjax_path`` for you and copy the necessary JavaScript and font
files to your output directory when you build your documentation as usual.

__ https://pypi.org/project/sphinx-mathjax-offline/
