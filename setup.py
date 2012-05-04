from setuptools import setup, find_packages
import os

version = '1.1'

tests_require = []

setup(name='redomino.advancedkeyword',
      version=version,
      description="Redomino Advanced Keyword Management",
      long_description=open("README.txt").read() + "\n" +
                       open(os.path.join("docs", "HISTORY.txt")).read(),
      # Get more strings from
      # http://pypi.python.org/pypi?:action=list_classifiers
      classifiers=[
        "Framework :: Plone",
        "Programming Language :: Python",
        ],
      keywords='',
      author='Davide Moro',
      author_email='davide.moro@redomino.com',
      url='https://github.com/redomino/redomino.advancedkeyword',
      license='GPL',
      packages=find_packages(exclude=['ez_setup']),
      namespace_packages=['redomino'],
      include_package_data=True,
      zip_safe=False,
      install_requires=[
          'setuptools',
          # -*- Extra requirements: -*-
          'z3c.jbot',
          'plone.browserlayer',
          'plone.indexer',
          'plone.app.vocabularies',
          'plone.app.z3cform',
      ],
      entry_points="""
      # -*- Entry points: -*-

      [z3c.autoinclude.plugin]
      target = plone
      """,
      tests_require=tests_require,
      extras_require = {
          'test': tests_require,
      },
#      setup_requires=["PasteScript"],
#      paster_plugins=["ZopeSkel"],
      )
