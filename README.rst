======
mycraft
======


.. image:: https://img.shields.io/pypi/v/mycraft.svg
        :target: https://pypi.python.org/pypi/mycraft

.. image:: https://img.shields.io/travis/cjp256/mycraft.svg
        :target: https://travis-ci.com/cjp256/mycraft

.. image:: https://readthedocs.org/projects/mycraft/badge/?version=latest
        :target: https://mycraft.readthedocs.io/en/latest/?badge=latest
        :alt: Documentation Status


.. image:: https://pyup.io/repos/github/cjp256/mycraft/shield.svg
     :target: https://pyup.io/repos/github/cjp256/mycraft/
     :alt: Updates



*craft tooling


* Free software: GNU General Public License v3
* Documentation: https://mycraft.readthedocs.io.


Example
--------

git clone git://github.com/cjp256/xcraft
git clone git://github.com/cjp256/mycraft

python3 -m venv ~/.venv/xcraft
. ~/.venv/xcraft/bin/activate

pip install -e xcraft
pip install -e mycraft

mycraft --provider=host craft
mycraft --provider=lxd craft

Credits
-------

This package was created with Cookiecutter_ and the `audreyr/cookiecutter-pypackage`_ project template.

.. _Cookiecutter: https://github.com/audreyr/cookiecutter
.. _`audreyr/cookiecutter-pypackage`: https://github.com/audreyr/cookiecutter-pypackage
