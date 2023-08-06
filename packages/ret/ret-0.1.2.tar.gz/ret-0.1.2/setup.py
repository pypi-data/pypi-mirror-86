# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['ret']

package_data = \
{'': ['*']}

entry_points = \
{'console_scripts': ['ret = ret.__main__:main']}

setup_kwargs = {
    'name': 'ret',
    'version': '0.1.2',
    'description': 'A pure-python command-line regular expression tool for stream filtering, extracting, and parsing.',
    'long_description': '===\nRet\n===\nA pure-python command-line regular expression tool for stream filtering, extracting,\nand parsing, designed to be minimal with an intuitive command-line interface.\n\nInstallation\n-------------\n\nYou can install this via\n\n.. code-block:: bash\n\n    python3 -m pip install ret\n    ✨🍰✨\n\n\nor using pipx\n\n.. code-block:: bash\n\n    pipx install ret\n    ✨🍰✨\n\nRet is pure python (3.6+) with no dependencies.\n\nUsage\n------\n\nExample\n~~~~~~~~\n\nYou can use ``Ret`` to extract text via regex capture groups:\n\n.. code-block:: bash\n\n    $ git branch\n    * master\n    $ git branch | ret "\\* (\\w+)" --group 1\n    master\n\n...finding all occurrences of a pattern:\n\n.. code-block:: bash\n\n    $ ls | ret ".*\\.py" findall\n    foo.py\n    bar.py\n\nand even all occurrences of a pattern with capture groups:\n\n.. code-block:: bash\n\n    $ ls | ret "(.*)\\.py" findall --group 1\n    foo\n    bar\n\nand much much more.\n\nBackground\n-------------\nI love ``grep``. But grep isn\'t really for text extraction.\n\nFor example, you cannot extract regexes via capture groups.\n\nSince I wanted that functionality, I decided to build this, ``Ret``.\n\nWhy the name?\n~~~~~~~~~~~~~\n\n``Ret`` is an acronym for **r**\\ egular **e**\\ xpression **t**\\ tool.\n\n\nWhy it can\'t replace grep (yet)\n~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~\n\n``Ret`` originally was designed to provide some features ``grep`` lacks.\nIt never intended to replace good ol\' ``grep``.\n\nGrep is great for searching directories while\n``ret`` (currently) can only read from a file or stdin.\n\nFurthermore, you cannot guarantee that ``ret`` is installed on the machine.\n\nAlso, ``Ret`` relies on the (slow) python regex engine.\n\nFeel free to contribute!\n',
    'author': 'Bryan Hu',
    'author_email': 'bryan.hu.2020@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/ThatXliner/ret/',
    'packages': packages,
    'package_data': package_data,
    'entry_points': entry_points,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
