.. image:: https://img.shields.io/pypi/v/jaraco.test.svg
   :target: `PyPI link`_

.. image:: https://img.shields.io/pypi/pyversions/jaraco.test.svg
   :target: `PyPI link`_

.. _PyPI link: https://pypi.org/project/jaraco.test

.. image:: https://dev.azure.com/jaraco/jaraco.test/_apis/build/status/jaraco.jaraco.test?branchName=master
   :target: https://dev.azure.com/jaraco/jaraco.test/_build/latest?definitionId=1&branchName=master

.. image:: https://img.shields.io/travis/jaraco/jaraco.test/master.svg
   :target: https://travis-ci.org/jaraco/jaraco.test

.. image:: https://img.shields.io/badge/code%20style-black-000000.svg
   :target: https://github.com/psf/black
   :alt: Code style: Black

.. .. image:: https://img.shields.io/appveyor/ci/jaraco/jaraco-test/master.svg
..    :target: https://ci.appveyor.com/project/jaraco/jaraco-test/branch/master

.. .. image:: https://readthedocs.org/projects/jaracotest/badge/?version=latest
..    :target: https://jaracotest.readthedocs.io/en/latest/?badge=latest

Plugins
=======

The 'enabler' plugin allows configuration of plugins if present, but omits the settings if the plugin is not present. For example, to configure black to be enabled if the plugin is present, but not when it is not, add the following to your pyproject.toml:

    [jaraco.test.pytest.plugins.black]
    addopts = "--black"
