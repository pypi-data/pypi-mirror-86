# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['nanocompore']

package_data = \
{'': ['*'], 'nanocompore': ['models/*']}

install_requires = \
['bedparse>=0.2,<0.3',
 'loguru>=0.5,<0.6',
 'matplotlib>=3.1,<3.2',
 'numpy>=1.19,<1.20',
 'pandas>=0.25,<0.26',
 'pyfaidx>=0.5,<0.6',
 'pyyaml>=5,<6',
 'scikit-learn>=0.23,<0.24',
 'scipy>=1.5,<1.6',
 'seaborn>=0,<1',
 'statsmodels>=0.12,<0.13',
 'tqdm>=4,<5']

entry_points = \
{'console_scripts': ['nanocompore = nanocompore.__main__:main']}

setup_kwargs = {
    'name': 'nanocompore',
    'version': '1.0.1',
    'description': 'Software package that identifies raw signal changes between two conditions from https://github.com/jts/nanopolish resquiggled dRNA-Seq data.',
    'long_description': '![Nanocompore](docs/pictures/Nanocompore_logo.png)\n\n---\n\n[![GitHub license](https://img.shields.io/github/license/tleonardi/nanocompore)](https://github.com/tleonardi/nanocompore/blob/master/LICENSE)\n[![Python](https://img.shields.io/badge/Python-%3E%3D3.6-yellow)](https://www.python.org/)\n[![BioRxiv](https://img.shields.io/badge/BioRxiv-10.1101%2F843136%20-red)](https://www.biorxiv.org/content/10.1101/843136v1.full)\n\n[![PyPI version](https://badge.fury.io/py/nanocompore.svg)](https://badge.fury.io/py/nanocompore)\n[![Downloads](https://pepy.tech/badge/nanocompore)](https://pepy.tech/project/nanocompore)\n[![Build Status](https://travis-ci.com/tleonardi/nanocompore.svg?token=2uTrW9fP9RypfMALjksc&branch=master)](https://travis-ci.com/tleonardi/nanocompore)\n\n---\n\n**Nanocompore identifies differences in ONT nanopore sequencing raw signal corresponding to RNA modifications by comparing 2 samples**\n\nNanocompore compares 2 ONT nanopore direct RNA sequencing datasets from different experimental conditions expected to have a significant impact on RNA modifications. It is recommended to have at least 2 replicates per condition. For example one can use a control condition with a significantly reduced number of modifications such as a cell line for which a modification writing enzyme was knocked-down or knocked-out. Alternatively, on a smaller scale transcripts of interests could be synthesized in-vitro.\n\n**Full documentation is available at http://nanocompore.rna.rocks**\n\n[![Nanocompore](docs/pictures/worflow.png)](http://nanocompore.rna.rocks)\n\n## Companion repositories\n\n* [NanoCompore_pipeline](https://github.com/tleonardi/nanocompore_pipeline): Nextflow pipeline to preprocess data for NanoCompore\n* [Nanocompore_analysis](https://github.com/tleonardi/nanocompore_paper_analyses): Analyses performed with Nanocompore for the BioRxiv preprint\n* [NanopolishComp](https://github.com/tleonardi/NanopolishComp): Collapse Nanopolish eventalign output per kmer, required before running NanoCompore\n\n## Main authors\n\n* Tommaso Leonardi - tom {at} tleo.io\n* Adrien Leger - aleg {at} ebi.ac.uk\n',
    'author': 'Tommaso Leonardi',
    'author_email': 'tom@itm6.xyz',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/tleonardi/nanocompore',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.6.1',
}


setup(**setup_kwargs)
