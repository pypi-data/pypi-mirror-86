# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['aiojarm']

package_data = \
{'': ['*']}

install_requires = \
['poetry-version>=0.1.5,<0.2.0']

setup_kwargs = {
    'name': 'aiojarm',
    'version': '0.1.0',
    'description': 'Async JARM client',
    'long_description': '# aiojarm\n\nAsync version of [JARM](https://github.com/salesforce/jarm).\n\n## Installation\n\n```bash\npip install aiojarm\n```\n\n## Usage\n\n```python\nimport asyncio\nimport aiojarm\n\nloop = asyncio.get_event_loop()\nfingerprints = loop.run_until_complete(\n    asyncio.gather(\n        aiojarm.scan("www.salesforce.com"),\n        aiojarm.scan("www.google.com"),\n        aiojarm.scan("www.facebook.com"),\n        aiojarm.scan("github.com"),\n    )\n)\nprint(fingerprints)\n# [\n#     (\n#         "www.salesforce.com",\n#         443,\n#         "23.42.156.194",\n#         "2ad2ad0002ad2ad00042d42d00000069d641f34fe76acdc05c40262f8815e5",\n#     ),\n#     (\n#         "www.google.com",\n#         443,\n#         "172.217.25.228",\n#         "27d40d40d29d40d1dc42d43d00041d4689ee210389f4f6b4b5b1b93f92252d",\n#     ),\n#     (\n#         "www.facebook.com",\n#         443,\n#         "31.13.82.36",\n#         "27d27d27d29d27d1dc41d43d00041d741011a7be03d7498e0df05581db08a9",\n#     ),\n#     (\n#         "github.com",\n#         443,\n#         "52.192.72.89",\n#         "29d29d00029d29d00041d41d0000008aec5bb03750a1d7eddfa29fb2d1deea",\n#     ),\n# ]\n```\n\n## License\n\nJARM is created by Salesforce\'s JARM team and it is licensed with 3-Clause "New" or "Revised" License.\n\n- https://github.com/salesforce/jarm/blob/master/LICENSE.txt\n',
    'author': 'Manabu Niseki',
    'author_email': 'manabu.niseki@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
