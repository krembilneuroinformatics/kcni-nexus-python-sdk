<p align="center"><a href="https://github.com/BlueBrain/nexus-sdk-js" target="_blank" rel="noopener noreferrer"><img src="/docs/_static/Blue-Brain-Nexus-Python-SDK-Github-Banner.jpg" alt="Nexus JS Banner"></a></p>

# Nexus Python SDK

KCNI-maintained version of the Python SDK for Blue Brain [Blue Brain Nexus](https://github.com/BlueBrain/nexus).

[Original Repository](#original-repository) |
[Getting Started](#getting-started) |
[Upgrade](#upgrade) |
[Contributing](#contributing)

---

## Original Repository

Original Python SDK can be found here: [Nexus Python SDK](https://github.com/BlueBrain/nexus-python-sdk).
Documentation for original version: https://bluebrain.github.io/nexus-python-sdk/.

## Getting Started

### Usage

````python
import nexussdk as nexus

nexus.client.NexusClient(DEPLOYMENT, TOKEN)
nexus.config.set_token(TOKEN)

nexus.permissions.fetch()
````

More examples in the folder [notebooks](./notebooks) and [tests](./tests).

Documentation: https://bluebrain.github.io/nexus-python-sdk/.

### Installation

**Development version**

```bash
pip install git+https://github.com/BlueBrain/nexus-python-sdk
```

**Development mode**

```bash
git clone https://github.com/bluebrain/nexus-python-sdk
pip install --editable nexus-python-sdk
```

**Requirements**

- [requests](http://docs.python-requests.org)
- [sseclient==0.0.22](https://pypi.org/project/sseclient/0.0.22/)

## Upgrade

```bash
pip install --upgrade nexus-sdk
```

## Contributing

### Styling

Follow [PEP 20](https://www.python.org/dev/peps/pep-0020/),
[PEP 8](https://www.python.org/dev/peps/pep-0008/), and
[PEP 257](https://www.python.org/dev/peps/pep-0257/), at least.

### Documentation

The documentation is auto-generated with [Sphinx](http://www.sphinx-doc.org).
To install it:

```bash
pip install nexus-sdk[doc]
```

**Update**

To add a new module to the API Reference, add the corresponding section in the
files `admin-reference.rst`, `kg-reference.rst`, or `iam-reference.rst` which 
are in the directory `docs-sources/sphix/source/`.

**Generate**

```bash
cd docs-source/sphinx
make html
```

**Deploy**

```bash
cp -R build/html/ ../../docs/
```

### Releasing

**Setup**

```bash
pip install --upgrade pip setuptools wheel twine
```

**Tagging**

```bash
git checkout master
git pull upstream master
git tag -a v<x>.<y>.<z> HEAD
git push upstream v<x>.<y>.<z>
```

**Building**

```bash
python setup.py sdist bdist_wheel
```

**Upload**

```bash
twine upload dist/*
```

**Cleaning**

```bash
rm -R build dist *.egg-info
```
