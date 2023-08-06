<p align="center">
<a href="https://apiclient.xaipient.com"><img src="./images/logo.png" height="200" alt="xac"></a>
</p>
<p align="center">
    <em>Powering your AI with human friendly explanations</em>
</p>

## Xaipient API Client (xac)
----
**Status: Alpha, Version: 0.3.0**

**Documentation**: <a href="https://xaipient.github.io/xaipient-docs/" target="_blank">https://xaipient.github.io/xaipient-docs/</a>

---

## Requirements

Python 3.6+

## Installation

```console
$ pip install xac
```



## Python API

```python
from xac import Explainer

Explainer.login('user@domain.com')

with Explainer() as german_explainer:
    german_explainer.from_config('tests/sample/configs/german-keras.yaml')
    global_imps =  german_explainer.get_global_importances()
    global_aligns =  german_explainer.get_global_alignments()
    global_rules = german_explainer.get_global_rules()
    local_attrs = german_explainer.get_local_attributions(feature_row=4)
    local_rules =  german_explainer.get_global_rules(feature_row=4)
    counterfactuals = german_explainer.get_counterfactuals(feature_row=4)
print(global_imps)
print(global_aligns)
print(global_rules)
print(local_attrs)
print(local_rules)
print(counterfactuals)
```

See Documentation for more details

## Commandline interface

```console
$ xac login --email user@domain.com
$ xac session init -f german-keras.yaml -n german_credit
$ xac job submit -s <SESSION_ID> -e local_attributions -e global_importances --start 4 --end 5
$ xac job output <JOB_ID> -o /tmp/explns.json
```

```
Commands:
  config    Generate Xaipient YAML config files for customization
  info      Display key information about API
  job       Manage and Generate Explanations with Xaipient API
  jobs      List explanation jobs.
  login     Login with email and password.
  logout    Logout and purge any tokens.
  session   Manage and Create Sessions for Explanations
  sessions  List all created sessions.
  version   Display current version of client and API.
```

See Documentation for more details
