# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['pyentrez', 'pyentrez.entrez', 'pyentrez.utils']

package_data = \
{'': ['*'], 'pyentrez': ['.vscode/*', 'config/*', 'logs/*']}

install_requires = \
['ConfigArgParse>=1.2.3,<2.0.0',
 'PyYAML>=5.3.1,<6.0.0',
 'biopython>=1.78,<2.0',
 'keyring>=21.5.0,<22.0.0',
 'loguru>=0.5.3,<0.6.0',
 'py-cui>=0.1.2,<0.2.0']

entry_points = \
{'console_scripts': ['run = pyEntrez:main']}

setup_kwargs = {
    'name': 'pyentrez',
    'version': '0.1.0',
    'description': 'pyEntrez tool suite wrapped in pyCUI TUI',
    'long_description': 'pyEntrez\n--------\n\n**pyEntrez** aims to be a user-friendly suite of Biopython’s Entrez\ntools that may be accessed from either the commandline in a script/arg\nfunction, or from a persistent Text User Interface (TUI). The current\nimplementation will extend to the full use of Entrez for publication\nbrowsing, and will offer features to automatically send query results to\na database of the user’s choice as well as facilitate database\nmanipulation.\n\nPlanned features include data interpretation with toolsets such as\nPandas. As well as incorporating text analysis and machine learning to\nflag abstracts that are pertinent to the research conducted by the user.\n\nUnplanned, but interesting, features would be to incorporate the rest of\nthe tools offered by Biopython in a one-stop shop.\n\nThe current implementation has been developed in Python 3 Win10 but\nshould work with Linux based OS (maybe with minor modifications in terms\nof printing and error handling.)\n\nMotivation\n----------\n\nAs a novice programmer in the medical science realm, I wanted to see if I could implement a suite of tools that could pull all of the Entrez functionality together under one  script, as well as manipulate the data pulled. I envision this script allowing for a much more rapid acquisition of relevant data for systemic reviews and meta-analysis, which is a process limited by the amount of research assistants and hours available to scrape and read abstracts.\n\nCode style\n----------\n\n|made-with-python|\n\nInstallation\n------------\n\nAPI Reference\n-------------\n\nHow to use?\n-----------\n\nCredits\n-------\n\nPowered by: py_CUI Python Command Line UI library:\nhttps://github.com/jwlodek/py_cui Docs:\nhttps://jwlodek.github.io/py_cui-docs\n\nBiopython library: https://github.com/biopython/biopython Docs:\nhttps://biopython.org\n\nLicense\n-------\n\nMIT © William Slattery 2020\n\n.. |made-with-python| image:: https://img.shields.io/badge/Made%20with-Python-1f425f.svg\n   :target: https://www.python.org/',
    'author': 'William Slattery',
    'author_email': 'slatte26@msu.edu',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/BGASM/pyEntrez',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
