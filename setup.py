""" EEA Similarity Installer
"""
import os
from os.path import join
from setuptools import setup, find_packages

NAME = 'eea.similarity'
PATH = NAME.split('.') + ['version.txt']
VERSION = open(join(*PATH)).read().strip()

setup(name=NAME,
      version=VERSION,
      description="A package that suggests similar titles to one being added",
      long_description=open("README.rst").read() + "\n" +
                       open(os.path.join("docs", "HISTORY.txt")).read(),
      classifiers=[
          "Framework :: Zope2",
          "Framework :: Zope3",
          "Framework :: Plone",
          "Framework :: Plone :: 4.0",
          "Framework :: Plone :: 4.1",
          "Framework :: Plone :: 4.2",
          "Programming Language :: Zope",
          "Programming Language :: Python",
          "Topic :: Software Development :: Libraries :: Python Modules",
          "License :: OSI Approved :: GNU General Public License (GPL)",
        ],
      keywords='eea cosine similarity plugins plone zope3',
      author='European Environment Agency',
      author_email="webadmin@eea.europa.eu",
      maintainer='Valentin Dumitru (Eau de Web)',
      maintainer_email='valentin.dumitru@eaudeweb.ro',
      download_url="http://pypi.python.org/pypi/eea.similarity",
      url='http://eea.github.com/docs/eea.similarity',
      license='GPL',
      packages=find_packages(exclude=['ez_setup']),
      namespace_packages=['eea'],
      include_package_data=True,
      zip_safe=False,
      install_requires=[
          'setuptools',
          # -*- Extra requirements: -*-
          'gensim',
          'stemming',
      ],
      extras_require={
          'test': [
              'plone.app.testing'
          ],
          'zope2': [
          ],
      },
      entry_points="""
      [z3c.autoinclude.plugin]
      target = plone
      """
      )
