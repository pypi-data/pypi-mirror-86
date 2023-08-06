# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['chaine']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'chaine',
    'version': '0.1.0',
    'description': 'A lightweight Linear-Chain Conditional Random Field',
    'long_description': '# A lightweight Linear-Chain Conditional Random Field\n\nThis is a modern, fast and no-dependency Python library implementing a linear-chain conditional random field for natural language processing tasks like named entity recognition or part-of-speech tagging.\n\n\n## Installation\n\nYou can install the latest stable version from [PyPI](https://pypi.org/project/chaine):\n\n```\n$ pip install chaine\n```\n\n\n## Example\n\n```python\n>>> import chaine\n>>> import datasets\n>>> data = datasets.load_dataset("germeval_14")\n>>> tokens = data["train"]["tokens"]\n>>> labels = data["train"]["ner_tags"]\n>>> crf = chaine.train(tokens, labels, max_iterations=100)\n>>> sequence = chaine.featurize(["todo", "todo", "todo"])\n>>> crf.predict(sequence)\n["O", "O", "B-PER"]\n```\n\n\n## Disclaimer\n\nThis library makes use of and is partially based on:\n\n- [CRFsuite](https://github.com/chokkan/crfsuite)\n- [libLBFGS](https://github.com/chokkan/liblbfgs)\n- [python-crfsuite](https://github.com/scrapinghub/python-crfsuite)\n- [sklearn-crfsuite](https://github.com/TeamHG-Memex/sklearn-crfsuite)\n',
    'author': 'Severin Simmler',
    'author_email': 'severin.simmler@posteo.de',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.8,<4.0',
}
from build import *
build(setup_kwargs)

setup(**setup_kwargs)
