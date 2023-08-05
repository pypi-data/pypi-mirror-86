# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['jupydocs']

package_data = \
{'': ['*']}

install_requires = \
['ipython>=7.19.0,<8.0.0', 'tabulate>=0.8.7,<0.9.0']

setup_kwargs = {
    'name': 'jupydocs',
    'version': '0.1.1',
    'description': 'Easy Python package documentation using markdown and jupyter',
    'long_description': '![jupydocs_logo](https://github.com/SamEdwardes/jupydocs/raw/main/website/static/img/jupydocs_logo_text.png)\n\n[![Netlify Status](https://api.netlify.com/api/v1/badges/6bc56cde-7bc0-492e-a357-7d2ca05004a3/deploy-status)](https://app.netlify.com/sites/jupydocs/deploys)\n\nThe easiest way to document your python library with jupyter and markdown.\n\n- [GitHub](https://github.com/SamEdwardes/jupydocs)\n- [docs](https://jupydocs.netlify.app/)\n- [PyPi](https://pypi.org/project/jupydocs/)\n\n```\nPleaes note jupydocs is currently under active development. \nIt can be used for testing, but should not be used for deployment. \nIt will change!\n```\n\n\n## Installation\n\n```bash\npip install jupydocs\n```\n\n## Quickstart\n\n\n```python\nfrom jupydocs.numpydocstring import NumpyDocString\n\ndef custom_sum(x, y):\n    """A new take on the class `sum` function.\n    \n    Does 1 + 1 always need to equal 2? Not anymore! Thanks to the `custom_sum`\n    function 1 + 1 will never equal 2 again.\n\n    Parameters\n    ----------\n    x : float\n        A number.\n    y : float\n        A number.\n\n    Returns\n    -------\n    num : Float\n        A new take on the traditional sum function. x * 2 + y * 3. Not at all\n        useful. But fun!\n        \n    Example\n    -------\n    >>> from examplepackage.example import custom_sum\n    >>> custom_sum(2, 3)\n    13    \n    """\n    return x * 2 + y * 3\n\ndocstring = NumpyDocString(custom_sum)\ndocstring.render_md()\n```\n\n\n\n\n## custom_sum\n\nA new take on the class `sum` function. \n\nDoes 1 + 1 always need to equal 2? Not anymore! Thanks to the `custom_sum` function 1 + 1 will never equal 2 again.\n\n### Parameters\n\n| NAME   | TYPE   | DESCRIPTION   |\n|:-------|:-------|:--------------|\n| x      | float  | A number.     |\n| y      | float  | A number.     |\n\n### Returns\n\n| NAME   | TYPE   | DESCRIPTION                                                                            |\n|:-------|:-------|:---------------------------------------------------------------------------------------|\n| num    | Float  | A new take on the traditional sum function. x * 2 + y * 3. Not at all useful. But fun! |\n\n### Example\n\n```python\n>>> from examplepackage.example import custom_sum\n>>> custom_sum(2, 3)\n13\n```\n\n\n\n',
    'author': 'SamEdwardes',
    'author_email': 'edwardes.s@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/SamEdwardes/jupydocs',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
