==============
EEA Similarity
==============
.. image:: https://ci.eionet.europa.eu/buildStatus/icon?job=eea/eea.similarity/develop
  :target: https://ci.eionet.europa.eu/job/eea/job/eea.similarity/job/develop/display/redirect
  :alt: develop
.. image:: https://ci.eionet.europa.eu/buildStatus/icon?job=eea/eea.similarity/master
  :target: https://ci.eionet.europa.eu/job/eea/job/eea.similarity/job/master/display/redirect
  :alt: master

Introduction
============

EEA Similarity is a Plone_ add-on which provides content suggestions based on similarity scores to a search string. It uses NLP algorithms like TF-IDF (frequency–inverse document frequency) and LSI (Latent Semantic Indexing).

Initial use case is to provide a list of possible duplicates when adding content (based on the entered title).

.. contents::


Installation
============

zc.buildout
-----------
If you are using `zc.buildout`_ and the `plone.recipe.zope2instance`_
recipe to manage your project, you can do this:

* Update your buildout.cfg file:

  * Add ``eea.similarity`` to the list of eggs to install
  * Tell the `plone.recipe.zope2instance`_ recipe to install a ZCML slug

  ::

    [instance]
    ...
    eggs =
      ...
      eea.similarity

    zcml =
      ...
      eea.similarity

* Re-run buildout, e.g. with::

  $ ./bin/buildout

You can skip the ZCML slug if you are going to explicitly include the package
from another package's configure.zcml file.


Getting started
===============

1. Go to **Site Setup > Add-ons** and install **EEA Similarity**
2. Create IDF index by calling **@@create_idf_index** Browser view on site root.
   If you have **plone.app.async** installed, it will add a daily job to async queue,
   otherwise you'll have to setup an external cron job to call this periodically.
3. Customize settings via Site Setup > EEA Similarity Settings


Dependencies
============

`EEA Similarity`_ has the following dependencies:
  - stemming
  - gensim (which in turn depends on numpy and scipy)

On CentOS you need to install:
  - blas-devel
  - lapack-devel
  - gcc-fortran

On Debian/Ubuntu you need to install:
  - libblas-dev
  - liblapack
  - gfortran

Possible issues with scipy and numpy:
-------------------------------------
Due to a bug in scipy, it is possible that the packages will not install when
running buildout. There are two solutions/options:

1. Install them with easy_install pip before running the buildout.
2. Update `zc.buildout`_ to version 2.9.0 and activate the wheel support via `buildout.wheel`_ and the dependencies will be installed normally.


Source code
===========

- `EEA on Github <https://github.com/eea/eea.similarity>`_


Copyright and license
=====================
The Initial Owner of the Original Code is European Environment Agency (EEA).
All Rights Reserved.

The EEA Similarity (the Original Code) is free software;
you can redistribute it and/or modify it under the terms of the GNU
General Public License as published by the Free Software Foundation;
either version 2 of the License, or (at your option) any later
version.

More details in License.txt

Funding
=======

EEA_ - European Environment Agency (EU)

.. _EEA: https://www.eea.europa.eu/
.. _`plone.recipe.zope2instance`: https://pypi.python.org/pypi/plone.recipe.zope2instance
.. _`zc.buildout`: https://pypi.python.org/pypi/zc.buildout
.. _`buildout.wheel`: https://pypi.python.org/pypi/buildout.wheel
.. _Plone: https://plone.org
