# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['genni', 'genni.griding', 'genni.nets']

package_data = \
{'': ['*']}

install_requires = \
['matplotlib>=3.3.2,<4.0.0',
 'numpy>=1.19.4,<2.0.0',
 'pandas>=1.1.4,<2.0.0',
 'plotly>=4.12.0,<5.0.0',
 'pyyaml>=5.3.1,<6.0.0',
 'ray[tune]>=1.0.0,<2.0.0',
 'tensorboard>=2.3.0,<3.0.0',
 'torch>=1.7.0,<2.0.0',
 'torchvision>=0.8.1,<0.9.0',
 'tqdm>=4.51.0,<5.0.0']

setup_kwargs = {
    'name': 'genni',
    'version': '1.0.0',
    'description': 'GENNI: Visualising the Geometry of Equivalences for Neural Network Identifiability',
    'long_description': '# [GENNI: Visualising the Geometry of Equivalences for Neural Network Identifiability](https://drive.google.com/file/d/1mGO-rLOZ-_TXu_-8KIfSUiFEqymxs2x5/view)\n\n## Disclaimer\n\nThis is code associated with the paper ["GENNI: Visualising the Geometry of Equivalences for Neural Network Identifiability,"](https://drive.google.com/file/d/1mGO-rLOZ-_TXu_-8KIfSUiFEqymxs2x5/view) published in the [NeurIPS](https://nips.cc/) Workshop on [Differential Geometry meets Deep Learning 2020](https://sites.google.com/view/diffgeo4dl/).\n\nIf you have any questions, please feel free to reach out to us or make an issue.\n\n## Preliminaries\n\nOur\n\n```\npip install -r requirements.txt\n```\n\n## Usage\n\nTo use our package...\n\n```\n<details on library import and script execution go here>\n```\n\nHow saving is done:\n\nResults are expected to saved in specific locations. If this code is not used to create equivalences classes, but the plotting functions want to be used, we advise to follow the structure laied out in get_grid.py and simply use the methods in interpolation.py which are agnostic to the saved locations.\n\n### Run experiment.py to produce elements in equivalence classes\n\n- To check if the elements converged to elements in the equivalence class, run stats_plotting.\n- Run the griding code to produce a set of elements in a subspace spanned by elements that were found.\n- Subset the set by elements wiht loss less than some epsilon and choose an appropriate plotting mechanism.\n\n### Getting directories and run IDs\n\nAfter creating an experiment this will be dumped to **GENNI_HOME/experiment** where **GENNI_HOME** is set in the **genni.yml** file. An easy way to get the experiment directory and the run ids is to use the _tree_ command line argument as follows:\n\n```sh\ntree $GENNI_HOME/experiments -d -L 3\n```\n\nAn example output looks like\n\n```sh\nexperiments\n└── Nov09_19-52-12_isak-arch\n    ├── models\n    │\xa0\xa0 └── 1604947934.637504\n    └── runs\n        └── 1604947934.637504\n```\n\nwhere `Nov09_19-52-12_isak-arch` is the identifier of the experiment and\n`1604947934.637504` is an ID of a hyperparameter setting of this experiment.\n\n## Citing\n\nIf you use GENNI anywhere in your work, please cite use using\n\n```\n@article{2020,\n    title={GENNI: Visualising the Geometry of Equivalences for Neural Network Identifiability},\n    author={Lengyel, Daniel and Petangoda, Janith and Falk, Isak and Highnam, Kate and Lazarou, Michalis and Kolbeinsson, Arinbjörn and Deisenroth, Marc Peter and Jennings, Nicholas R.},\n    booktitle={NeurIPS Workshop on Differential Geometry meets Deep Learning},\n    year={2020}\n}\n```\n',
    'author': 'Arinbjörn Kolbeinsson',
    'author_email': None,
    'maintainer': 'Isak Falk',
    'maintainer_email': 'ucabitf@ucl.ac.uk',
    'url': 'https://github.com/Do-Not-Circulate/GENNI_public',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<3.9',
}


setup(**setup_kwargs)
