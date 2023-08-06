# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['pydantic_annotated']

package_data = \
{'': ['*']}

install_requires = \
['pydantic']

setup_kwargs = {
    'name': 'pydantic-annotated',
    'version': '0.0.1a0',
    'description': 'Generate Pydantic Fields with typing.Annotated',
    'long_description': '# pydantic-annotated\n\nProof of concept [Decomposing Field components into Annotated](https://github.com/samuelcolvin/pydantic/issues/2129).\n\n```python\nfrom typing import Annotated\n\nfrom pydantic_annotated import BaseModel, Description, FieldAnnotationModel\n\n\nclass PII(FieldAnnotationModel):\n    status: bool\n\n\nclass ComplexAnnotation(FieldAnnotationModel):\n    x: int\n    y: int\n\n\nclass Patient(BaseModel):\n    name: str\n    condition: Annotated[\n        str,\n        ComplexAnnotation(x=1, y=2),\n        Description("Patient condition"),\n        PII(status=True),\n    ]\n```\n',
    'author': 'Jacob Hayes',
    'author_email': 'jacob.r.hayes@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'http://github.com/JacobHayes/pydantic-annotated',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
