# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['sati']

package_data = \
{'': ['*']}

install_requires = \
['matplotlib>=3.3.1,<4.0.0',
 'numexpr>=2.7.1,<3.0.0',
 'numpy>=1.18.0,<2.0.0',
 'scipy>=1.5.0,<2.0.0']

setup_kwargs = {
    'name': 'sati',
    'version': '1.0.0',
    'description': 'Statistical analysis of topographic image',
    'long_description': 'Sati\n====\nStatistical analysis of Topographic Image\n\nThis package provides\n\n* subtracting background (a polynomial surface, logarithmic decays, exponential decays)\n* labeling terraces\n* estimating terrace heights\n* estimating a unit height of steps\n\nThe subtraction is possible even in the presence of steps.\n\nInstall\n-------\nYou can install the package from the git repogitory using ``pip``\n::\n\n  $ pip install sati\n\nRequirements\n------------\nSati requires the following dependencies:\n\n* python 3.8\n* matplotlib\n* numexpr\n* numpy\n* scipy\n\nDocuments\n---------\nThe usage examples and the API documentation are available at https://yuksk.github.io/sati/index.html\n\n\n',
    'author': 'Yuhki Kohsaka',
    'author_email': 'yuhki.kohsaka@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/yuksk/sati/',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
