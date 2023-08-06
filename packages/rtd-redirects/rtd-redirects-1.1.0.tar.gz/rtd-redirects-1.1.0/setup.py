# -*- coding: utf-8 -*-
from setuptools import setup

modules = \
['rtd_redirects']
install_requires = \
['click>=7.1.2,<8.0.0',
 'cssselect>=1.1.0,<2.0.0',
 'lxml>=4.6.1,<5.0.0',
 'pyaml>=20.4.0,<21.0.0',
 'requests>=2.25.0,<3.0.0']

entry_points = \
{'console_scripts': ['rtd-redirects = rtd_redirects:main']}

setup_kwargs = {
    'name': 'rtd-redirects',
    'version': '1.1.0',
    'description': 'Manage redirects in the ReadTheDocs admin, programmatically',
    'long_description': 'rtd-redirects\n=============\n\nManage redirects in the `ReadTheDocs <http://readthedocs.org/>`__ admin, programmatically. Addressing the `rtfd/readthedocs.org#2904 <https://github.com/rtfd/readthedocs.org/issues/2904>`__ issue.\n\nInstallation\n------------\n\nRequires **Python 3.6** and higher.\n\n.. code:: sh\n\n    $ pip install rtd-redirects\n\nUsage\n-----\n\n.. code:: sh\n\n    $ rtd-redirects project-name ./redirects.yml --username=honzajavorek\n\nUploads redirects defined in the ``redirects.yml`` file to ReadTheDocs redirects administration of the ``project-name`` project.\n\nThe tool uses ReadTheDocs\' HTML interface (there\'s no official API for redirects), so you need to provide your username and password. HTTPS is used to transfer the credentials to ReadTheDocs.\n\n``rtd-redirects`` tries to be idempotent, i.e. you can run it several times in row and it should always end with the same results. If there are any redirects with the same source path, the tool will replace them with whatever is defined in the ``redirects.yml`` file. Existing redirects which do not collide with contents of ``redirects.yml`` won\'t be affected.\n\nredirects.yml\n-------------\n\nOnly **page redirects** are supported at the moment. The format of the file is as follows:\n\n.. code:: yaml\n\n    redirects:\n      # we\'ve migrated from MkDocs to Sphinx\n      "/example/": "/example.html"\n      "/python/": "/python.html"\n\n      # page removed in favor of section\n      "/green.html": "/colors.html#green"\n\n      # only for convenience\n      "/praha.html": "/prague.html"\n\nWhy `YAML <https://en.wikipedia.org/wiki/YAML>`__? Because it\'s easy to read by humans, easy to write by humans, and above all, it has support for comments. Redirects are *corrections* and you should document why they\'re necessary.\n\n\nUsage with ReadTheDocs PRO\n--------------------------\n\nIf you are using a commercial edition of the RTD (from ``readthedocs.com`` instead of ``readthedocs.org``), please specify ``--pro`` flag in the command, like this\n\n.. code:: sh\n\n    $ rtd-redirects project-name ./redirects.yml --username=honzajavorek --pro\n\nThere is also an opposite flag ``--free`` which is added by default, so can be omitted\n\n\nLicense: MIT\n------------\n\n© 2017-? Honza Javorek mail@honzajavorek.cz\n\nThis work is licensed under `MIT\nlicense <https://en.wikipedia.org/wiki/MIT_License>`__.\n',
    'author': 'Honza Javorek',
    'author_email': 'mail@honzajavorek.cz',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/honzajavorek/rtd-redirects',
    'py_modules': modules,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
