============
yaml-patcher
============


.. image:: https://img.shields.io/pypi/v/yaml_patcher.svg
        :target: https://pypi.python.org/pypi/yaml_patcher

.. image:: https://img.shields.io/travis/albertoeaf/yaml_patcher.svg
        :target: https://travis-ci.com/albertoeaf/yaml_patcher

.. image:: https://readthedocs.org/projects/yaml-patcher/badge/?version=latest
        :target: https://yaml-patcher.readthedocs.io/en/latest/?badge=latest
        :alt: Documentation Status




Patch yaml files.


* Free software: Apache Software License 2.0
* Documentation: https://yaml-patcher.readthedocs.io.

Installation
------------

.. code:: bash

        pip install yaml_patcher


Features
--------

Patch a YAML configuration file with another that specifies the transformations.
For now only supports a replace operation with a literal path.

Follows the format in ``https://github.com/krishicks/yaml-patch``.

To run just use:

.. code:: bash

        yaml_patcher base.yaml patch.yaml patched_output.yaml

Credits
-------

This package was created with Cookiecutter_ and the `audreyr/cookiecutter-pypackage`_ project template.

.. _Cookiecutter: https://github.com/audreyr/cookiecutter
.. _`audreyr/cookiecutter-pypackage`: https://github.com/audreyr/cookiecutter-pypackage
