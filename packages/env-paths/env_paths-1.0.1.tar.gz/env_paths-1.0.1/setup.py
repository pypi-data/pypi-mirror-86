# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['env_paths']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'env-paths',
    'version': '1.0.1',
    'description': 'Returns the directory where the cache is located. This is different for each os.',
    'long_description': "# env-paths <!-- TODO: badge -->\n\nThis package is a modified [sindresorhus/env\\-paths from nodejs](https://github.com/sindresorhus/env-paths) for python.\n\nReturns the directory where the cache is located. This is different for each os.\n\n\n\n## Install\n\n```\n$ pip install env-paths\n```\n\n\n## Usage\n\n```python\nfrom env_paths import env_paths\n\npaths = env_paths('MyApp')\npaths.data\n# => '/home/atu4403/.local/share/MyApp-python'\n\npaths.config\n# => '/home/atu4403/.config/MyApp-python'\n```\n\n## Related\n- [sindresorhus/env\\-paths: Get paths for storing things like data, config, cache, etc](https://github.com/sindresorhus/env-paths)\n\n\n## License\n\nMIT © [atu4403](https://github.com/atu4403)",
    'author': 'atu4403',
    'author_email': '73111778+atu4403@users.noreply.github.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/atu4403',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
