# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['modularyze', 'tests']

package_data = \
{'': ['*']}

install_requires = \
['Jinja2>=2.11.2,<3.0.0', 'ruamel.yaml>=0.16.12,<0.17.0']

setup_kwargs = {
    'name': 'modularyze',
    'version': '0.1.0',
    'description': 'Top-level package for modularyze.',
    'long_description': '==========\nModularyze\n==========\n\n\n.. image:: https://img.shields.io/pypi/v/modularyze.svg\n        :target: https://pypi.python.org/pypi/modularyze\n\n.. image:: https://img.shields.io/travis/jungerm2/modularyze.svg\n        :target: https://travis-ci.com/jungerm2/modularyze\n\n.. image:: https://readthedocs.org/projects/modularyze/badge/?version=latest\n        :target: https://modularyze.readthedocs.io/en/latest/?badge=latest\n        :alt: Documentation Status\n\n\n\n\nModularyze is a modular, composable and dynamic configuration engine that mixes the power of dynamic webpage rendering with that of YAML. It relies on Jinja_ and `ruamel.yaml`_ and inherits their flexibility.\n\n\nQuick Start\n-----------\n\nInstallation\n^^^^^^^^^^^^\n\nTo install the latest version of modularyze, run this command in your terminal:\n\n.. code-block:: console\n\n    $ pip install modularyze\n\n\nExample\n^^^^^^^\n\nThe Modularize package exposes one central config-builder class called ConfBuilder_. Using this class you can register arbitrary constructors and callables, render templated multi-file and dynamic configs, instantiate them and compare configs by hash or their normalized form.\n\nTo use modularyze in a project simply import it, register any callables your config might be using and point it to your configuration file. From there you can simply call build_ to build the config.\n\nA simple example where we instantiate a machine learning pipeline could look something like this:\n\n.. code-block::\n\n    # File: imagenet.yaml\n\n    {% set use_pretrained = use_pretrained | default(True) %}\n    {% set imagenet_root = imagenet_root | default(\'datasets/imagenet\') %}\n\n    network: &network\n        !torchvision.models.resnet18\n        pretrained: {{ use_pretrained }}\n\n    val_transforms: &val_transforms\n        !torchvision.transforms.Compose\n        - !torchvision.transforms.Resize [256]\n        - !torchvision.transforms.CenterCrop [224]\n        - !torchvision.transforms.ToTensor\n\n    dataset: &dataset\n        !torchvision.transforms.datasets.ImageNet\n        args:\n          - {{ imagenet_root }}\n        kwargs:\n          split: \'val\'\n          transforms: *val_transforms\n\n\n.. code-block:: python\n\n    import torchvision\n    from modularyze import ConfBuilder\n\n    builder = ConfBuilder()\n    builder.register_multi_constructors_from_modules(torchvision)\n    conf = builder.build(\'imagenet.yaml\')\n\nNow the ``conf`` object is a python dictionary containing a fully initialized model, dataset and validation transforms. What about if you want to change a parameter on the fly? Say the imagenet folder changes? Easy, simply pass in a context:\n\n.. code-block:: python\n\n    conf = builder.build(\'imagenet.yaml\', context={"imagenet_root": "new/path/to/dataset"})\n\nIn this way ypu can easily parameterize you configuration files. The provided context is usually a dictionary but it can even be the path to a (non-parameterized/vanilla) YAML file.\n\nWhat about if we have the configuration for a model trainer in a different file? Imagine the file ``trainer.yaml`` instantiates a neural network trainer instance, we can include it by adding the following line to the above config file:\n\n.. code-block:: jinja\n\n    {% include \'trainer.yaml\' %}\n\nThere are many more neat things you can do when you combine the powers of YAML and Jinja, please refer to the documentation_ for more.\n\n\n.. _Jinja: https://jinja.palletsprojects.com/en/2.11.x/\n.. _`ruamel.yaml`: https://pypi.org/project/ruamel.yaml/\n.. _documentation: https://modularyze.readthedocs.io/en/latest/\n.. _ConfBuilder: https://modularyze.readthedocs.io/en/latest/api.html#modularyze.modularyze.ConfBuilder/\n.. _build: https://modularyze.readthedocs.io/en/latest/api.html#modularyze.modularyze.ConfBuilder.build/\n',
    'author': 'Sacha Jungerman',
    'author_email': 'jungerm2@illinois.edu',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/jungerm2/modularyze',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
