# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['mafe', 'mafe.mafe', 'mafe.process', 'mafe.scan']

package_data = \
{'': ['*']}

install_requires = \
['audio-metadata>=0.11.1,<0.12.0',
 'audioread>=2.1.8,<3.0.0',
 'click>=7.1.2,<8.0.0',
 'librosa>=0.7.2,<0.8.0',
 'numba>=0.49.1,<0.50.0',
 'numpy>=1.18.5,<2.0.0',
 'pandas>=1.0.4,<2.0.0',
 'python-magic>=0.4.18,<0.5.0',
 'scikit-learn>=0.23.1,<0.24.0',
 'scipy>=1.4.1,<2.0.0']

entry_points = \
{'console_scripts': ['process = mafe.mafe.mafe_process:cli',
                     'scan = mafe.mafe.mafe_scan:scan_folders']}

setup_kwargs = {
    'name': 'mafe',
    'version': '0.1.15',
    'description': 'Music Audio Feature Extractor',
    'long_description': '# Music Audio Feature Extractor\n\n## `mafe_scan.py`\n\n```bash\n$ mafe_scan.py --help\nUsage: mafe_scan.py [OPTIONS]\n\nOptions:\n  -f, --base-folders TEXT  Directory to scan  [required]\n  -p, --parallel           Use parallel execution\n  -q, --quiet              Suppress warnings and progress messages\n  --help                   Show this message and exit.\n```',
    'author': 'Lene Preuss',
    'author_email': 'lene.preuss@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://gitlab.com/lilacashes/mafe',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
