# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['artisan']

package_data = \
{'': ['*']}

install_requires = \
['cbor2>=5.2,<6.0', 'numpy>=1.19,<2.0', 'typing-extensions>=3.7,<4.0']

extras_require = \
{':python_version >= "3.6" and python_version < "3.7"': ['contextvars>=2.4,<3.0'],
 'docs': ['sphinx>=3,<4']}

setup_kwargs = {
    'name': 'artisan-builder',
    'version': '0.3.0',
    'description': 'A build system for explainable science',
    'long_description': "Artisan\n=======\n\nArtisan is a lightweight experiment-management library with support for gradual\ntyping. It allows you to write code like this:\n\n.. code-block:: python3\n\n  class SineWave(artisan.Artifact):\n      'sin(2πf⋅t + φ) for t ∈ [0, 1sec), sampled at 44.1kHz.'\n\n      class Spec(Protocol):\n          f: float; 'Frequency'\n          φ: float = 0.0; 'Phase shift'\n\n      def __init__(self, spec: Spec) -> None:\n          self.t = np.linspace(0, 1, 44100)\n          self.x = np.sin(2 * np.pi * spec.f * self.t + spec.φ)\n\nto generate file trees like this:\n\n.. code-block:: sh\n\n  ├── SineWave_0000/\n  │\xa0\xa0 ├── _meta_.json\n  │\xa0\xa0 ├── t.cbor\n  │\xa0\xa0 └── x.cbor\n  └── SineWave_0001/\n      ├── _meta_.json\n      ├── t.cbor\n      └── x.cbor\n\nthat can be viewed as customizable, live-updated, interactive documents like\nthis:\n\n*-- artisan-ui screenshot --*\n\nto facilitate an explorable, explainable, composable-component-based approach to\nscientific, analytical, and artistic programming. Complete documentation is\navailable on `Read the Docs <https://artisan.readthedocs.io/en/latest/>`_.\n\n\n\nInstallation\n------------\n\n.. code-block:: shell\n\n  > pip install artisan-builder\n\nArtisan works with CPython and PyPy 3.6+.\n\n\n\nDevelopment\n-----------\n\nTo install the project's dependencies:\n\n  - Install `Python 3.6+ <https://www.python.org/downloads/>`_.\n  - Install `Poetry <https://python-poetry.org/docs/#installation>`_.\n  - Run `poetry install --no-root`.\n\nTo run the test suite::\n\n  > poetry run pytest\n\nTo build the HTML documentation::\n\n  > poetry run task build-docs\n\nTo build the HTML documentation with live-previewing::\n\n  > poetry run task serve-docs\n",
    'author': 'Mason McGill',
    'author_email': 'mmcgill@caltech.edu',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'extras_require': extras_require,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
