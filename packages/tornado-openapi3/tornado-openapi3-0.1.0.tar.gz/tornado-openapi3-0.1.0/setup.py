# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['tornado_openapi3']

package_data = \
{'': ['*']}

install_requires = \
['openapi-core>=0.13.4,<0.14.0', 'tornado>=4,<7']

setup_kwargs = {
    'name': 'tornado-openapi3',
    'version': '0.1.0',
    'description': 'Tornado OpenAPI 3 request and response validation library',
    'long_description': '===================\n Tornado OpenAPI 3\n===================\n\nTornado OpenAPI 3 request and response validation library.\n\nProvides integration between the `Tornado`_ web framework and `Openapi-core`_\nlibrary for validating request and response objects against an `OpenAPI 3`_\nspecification.\n\n\n.. _Tornado: https://www.tornadoweb.org/\n.. _Openapi-core: https://github.com/p1c2u/openapi-core\n.. _OpenAPI 3: https://swagger.io/specification/\n',
    'author': 'Correl Roush',
    'author_email': 'correl@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
