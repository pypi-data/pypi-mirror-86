# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['xac',
 'xac.api',
 'xac.api.auth',
 'xac.api.resources',
 'xac.qexplain',
 'xac.utils']

package_data = \
{'': ['*'], 'xac.api': ['schema/*']}

install_requires = \
['alive-progress>=1.6.1,<2.0.0',
 'dynaconf>=3.1.1,<4.0.0',
 'halo>=0.0.30,<0.0.31',
 'httpx>=0.15.5,<0.16.0',
 'humanize>=3.0.0,<4.0.0',
 'munch>=2.5.0,<3.0.0',
 'pandas>=1.1.3,<2.0.0',
 'pygments>=2.7.1,<3.0.0',
 'safer>=4.1.2,<5.0.0',
 'smart_open[all]>=2.2.1,<3.0.0',
 'tabulate>=0.8.7,<0.9.0',
 'typer[all]>=0.3.2,<0.4.0',
 'yamale>=3.0.4,<4.0.0',
 'yarl>=1.6.0,<2.0.0']

entry_points = \
{'console_scripts': ['xac = xac.main:app']}

setup_kwargs = {
    'name': 'xac',
    'version': '0.3.0',
    'description': 'Client for Xaipient Explainability REST API',
    'long_description': '<p align="center">\n<a href="https://apiclient.xaipient.com"><img src="./images/logo.png" height="200" alt="xac"></a>\n</p>\n<p align="center">\n    <em>Powering your AI with human friendly explanations</em>\n</p>\n\n## Xaipient API Client (xac)\n----\n**Status: Alpha, Version: 0.3.0**\n\n**Documentation**: <a href="https://xaipient.github.io/xaipient-docs/" target="_blank">https://xaipient.github.io/xaipient-docs/</a>\n\n---\n\n## Requirements\n\nPython 3.6+\n\n## Installation\n\n```console\n$ pip install xac\n```\n\n\n\n## Python API\n\n```python\nfrom xac import Explainer\n\nExplainer.login(\'user@domain.com\')\n\nwith Explainer() as german_explainer:\n    german_explainer.from_config(\'tests/sample/configs/german-keras.yaml\')\n    global_imps =  german_explainer.get_global_importances()\n    global_aligns =  german_explainer.get_global_alignments()\n    global_rules = german_explainer.get_global_rules()\n    local_attrs = german_explainer.get_local_attributions(feature_row=4)\n    local_rules =  german_explainer.get_global_rules(feature_row=4)\n    counterfactuals = german_explainer.get_counterfactuals(feature_row=4)\nprint(global_imps)\nprint(global_aligns)\nprint(global_rules)\nprint(local_attrs)\nprint(local_rules)\nprint(counterfactuals)\n```\n\nSee Documentation for more details\n\n## Commandline interface\n\n```console\n$ xac login --email user@domain.com\n$ xac session init -f german-keras.yaml -n german_credit\n$ xac job submit -s <SESSION_ID> -e local_attributions -e global_importances --start 4 --end 5\n$ xac job output <JOB_ID> -o /tmp/explns.json\n```\n\n```\nCommands:\n  config    Generate Xaipient YAML config files for customization\n  info      Display key information about API\n  job       Manage and Generate Explanations with Xaipient API\n  jobs      List explanation jobs.\n  login     Login with email and password.\n  logout    Logout and purge any tokens.\n  session   Manage and Create Sessions for Explanations\n  sessions  List all created sessions.\n  version   Display current version of client and API.\n```\n\nSee Documentation for more details\n',
    'author': 'Xaipient Team',
    'author_email': 'team@xaipient.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/xaipient/xac',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.6.1,<4.0.0',
}


setup(**setup_kwargs)
