==========
EEA Similarity
==========

Introduction
============

EEA Similarity provides cosine-based suggestions to a search string. Initial
use is to provide a list of possible duplicates when adding content (based on
the entered title)

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

Dependencies
============

`EEA Similarity`_ has the following dependencies:
  - stemming
  - gensim (which in turn depends on numpy and scipy

Possible issues with scipy:
--------------------------
Due to a bug in scipy, it is possible that the package will not install when
running buildout. The only reliable solution was to install it with easy_install
/ pip before running the buildout.


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

Contributor(s):
---------------

- Valentin Dumitru (Eau de Web)


More details under docs/License.txt

Funding
=======

EEA_ - European Environment Agency (EU)

.. _EEA: http://www.eea.europa.eu/
.. _`eea.tags`: http://eea.github.com/docs/eea.tags
.. _`plone.recipe.zope2instance`: http://pypi.python.org/pypi/plone.recipe.zope2instance
.. _`zc.buildout`: http://pypi.python.org/pypi/zc.buildout
