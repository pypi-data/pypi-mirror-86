.. image:: https://user-images.githubusercontent.com/21954664/84388841-84b4cc80-abf5-11ea-83f3-b8ce8de36e25.png
    :target: https://mlf-core.com
    :alt: mlf-core logo

|

========
mlf-core
========

.. image:: https://github.com/mlf-core/mlf-core/workflows/Build%20mlf-core%20Package/badge.svg
        :target: https://github.com/mlf-core/mlf-core/workflows/Build%20mlf-core%20Package/badge.svg
        :alt: Github Workflow Build mlf-core Status

.. image:: https://github.com/mlf-core/mlf-core/workflows/Run%20mlf-core%20Tox%20Test%20Suite/badge.svg
        :target: https://github.com/mlf-core/mlf_core/workflows/Run%20mlf-core%20Tox%20Test%20Suite/badge.svg
        :alt: Github Workflow Tests Status

.. image:: https://img.shields.io/pypi/v/mlf-core.svg
        :target: https://pypi.python.org/pypi/mlf-core
        :alt: PyPI

.. image:: https://img.shields.io/discord/742367395196305489?color=passing
        :target: https://discord.gg/Mv8sAcq
        :alt: Discord

.. image:: https://readthedocs.org/projects/mlf-core/badge/?version=latest
        :target: https://mlf-core.readthedocs.io/en/latest/?badge=latest
        :alt: Documentation Status

.. image:: https://flat.badgen.net/dependabot/thepracticaldev/dev.to?icon=dependabot
        :target: https://flat.badgen.net/dependabot/thepracticaldev/dev.to?icon=dependabot
        :alt: Dependabot Enabled


Fully GPU deterministic machine learning project templates using MLflow_.

* Free software: Apache2.0
* Documentation: https://mlf-core.readthedocs.io.

.. image:: https://user-images.githubusercontent.com/21954664/94257992-7a140e00-ff2c-11ea-8059-216a31c62ef1.gif
    :target: https://user-images.githubusercontent.com/21954664/94257992-7a140e00-ff2c-11ea-8059-216a31c62ef1.gif
    :alt: mlf-core create gif

Features
--------

* Jumpstart your machine learning project with fully fledged, multi GPU enabled mlflow project templates
* Pytorch, Tensorflow, XGBoost supported
* mlflow templates are fully GPU deterministic with system-intelligence
* Conda and Docker support out of the box

.. figure:: https://user-images.githubusercontent.com/21954664/98472352-c2dd0900-21f2-11eb-9fe3-929b2a21bd4c.png
   :scale: 100 %
   :alt: mlf-core summary

   mlf-core enables deterministic machine learning. MLflow and a provided Read the Docs setup ensure that all hyperparameters, metrics and model details are well documented.
   Reproducible environments are provided with the use of Conda and Docker. Finally, the mlf-core ecosystem ensures that all library specific settings required for determinism are enabled,
   no non-deterministic algorithms are used and that the used hardware is tracked.

Credits
-------

Primary idea and main development by `Lukas Heumos <https://github.com/zethson/>`_.
This package was created with cookietemple_ based on a modified `audreyr/cookiecutter-pypackage`_ project template using Cookiecutter_.

.. _MLflow: https://mlflow.org
.. _cookietemple: https://cookietemple.com
.. _Cookiecutter: https://github.com/audreyr/cookiecutter
.. _`audreyr/cookiecutter-pypackage`: https://github.com/audreyr/cookiecutter-pypackage
