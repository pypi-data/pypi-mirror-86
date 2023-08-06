# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['sadice']

package_data = \
{'': ['*']}

install_requires = \
['torch>=1.0.0,<2.0.0']

setup_kwargs = {
    'name': 'sadice',
    'version': '0.1.3',
    'description': 'Self-adjusting Dice Loss implementation',
    'long_description': '# Self-adjusting Dice Loss\n\nThis is an unofficial PyTorch implementation of the \n[Dice Loss for Data-imbalanced NLP Tasks](https://arxiv.org/abs/1911.02855) paper.\n\n## Usage\n\nInstallation\n\n```bash\npip install sadice\n```\n\n### Text classification example\n\n```python\nimport torch\nfrom sadice import SelfAdjDiceLoss\n\ncriterion = SelfAdjDiceLoss()\n# (batch_size, num_classes)\nlogits = torch.rand(128, 10, requires_grad=True)\ntargets = torch.randint(0, 10, size=(128, ))\n\nloss = criterion(logits, targets)\nloss.backward()\n```\n\n### NER example\n\n```python\nimport torch\nfrom sadice import SelfAdjDiceLoss\n\ncriterion = SelfAdjDiceLoss(reduction="none")\n# (batch_size, num_tokens, num_classes)\nlogits = torch.rand(128, 40, 10, requires_grad=True)\ntargets = torch.randint(0, 10, size=(128, 40))\n\nloss = criterion(logits.view(-1, 10), targets.view(-1))\nloss = loss.reshape(-1, 40).mean(-1).mean()\nloss.backward()\n```',
    'author': 'Ivan Fursov',
    'author_email': 'fursovia@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/fursovia/self-adj-dice',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.6.1,<4.0.0',
}


setup(**setup_kwargs)
