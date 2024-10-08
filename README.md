# Prowlarr Collection for Ansible
[![CI](https://github.com/devopsarr/ansible-collection-prowlarr/workflows/CI/badge.svg?event=push)](https://github.com/devopsarr/ansible-collection-prowlarr/actions) [![Codecov](https://img.shields.io/codecov/c/github/devopsarr/ansible-collection-prowlarr)](https://codecov.io/gh/adevopsarr/ansible-collection-prowlarr)

Ansible collection for Prowlarr based on [prowlarr-py SDK](https://github.com/devopsarr/prowlarr-py)
## Code of Conduct

We follow the [Ansible Code of Conduct](https://docs.ansible.com/ansible/devel/community/code_of_conduct.html) in all our interactions within this project.

If you encounter abusive behavior, please refer to the [policy violations](https://docs.ansible.com/ansible/devel/community/code_of_conduct.html#policy-violations) section of the Code for information on how to raise a complaint.

## Communication

<!--TODO: add devopsarr-->

For more information about communication, refer to the [Ansible Communication guide](https://docs.ansible.com/ansible/devel/community/communication.html).

## Contributing to this collection

The content of this collection is made by people like you, a community of individuals collaborating on making the world better through developing automation software.

We are actively accepting new contributors.

Any kind of contribution is very welcome.

You don't know how to start? Refer to our [contribution guide](CONTRIBUTING.md)!

We use the following guidelines:

* [CONTRIBUTING.md](CONTRIBUTING.md)
* [REVIEW_CHECKLIST.md](REVIEW_CHECKLIST.md)
* [Ansible Community Guide](https://docs.ansible.com/ansible/latest/community/index.html)
* [Ansible Development Guide](https://docs.ansible.com/ansible/devel/dev_guide/index.html)
* [Ansible Collection Development Guide](https://docs.ansible.com/ansible/devel/dev_guide/developing_collections.html#contributing-to-collections)

## Collection maintenance

The current maintainers are listed in the [MAINTAINERS](MAINTAINERS) file. If you have questions or need help, feel free to mention them in the proposals.

To learn how to maintain / become a maintainer of this collection, refer to the [Maintainer guidelines](MAINTAINING.md).

## Governance

The process of decision making in this collection is based on discussing and finding consensus among participants.

Every voice is important. If you have something on your mind, create an issue or dedicated discussion and let's discuss it!


## Ansible version compatibility

Tested with the three latest Ansible Core releases, and the current development version of Ansible. Ansible Core versions before 2.11.0 are not supported.

## Python version compatibility

Tested with the 3 latest compatible Python versions.

## Included content
See the complete list of collection content in the [Plugin Index](https://devopsarr.github.io/ansible-doc/collections/devopsarr/prowlarr/index.html#plugins-in-devopsarr-prowlarr).

### Installing the Collection from Ansible Galaxy

Before using this collection, you need to install it with the Ansible Galaxy command-line tool:
```bash
ansible-galaxy collection install devopsarr.prowlarr
```

You can also include it in a `requirements.yml` file and install it with `ansible-galaxy collection install -r requirements.yml`, using the format:
```yaml
---
collections:
  - name: devopsarr.prowlarr
```

Note that if you install the collection from Ansible Galaxy, it will not be upgraded automatically when you upgrade the `ansible` package. To upgrade the collection to the latest available version, run the following command:
```bash
ansible-galaxy collection install devopsarr.prowlarr --upgrade
```

You can also install a specific version of the collection, for example, if you need to downgrade when something is broken in the latest version (please report an issue in this repository). Use the following syntax to install version `0.1.0`:

```bash
ansible-galaxy collection install devopsarr.prowlarr:==0.1.0
```

See [Ansible Using collections](https://docs.ansible.com/ansible/devel/user_guide/collections_using.html) for more details.

The python module dependencies are not installed by `ansible-galaxy`.  They can
be manually installed using pip:

    pip install -r requirements.txt

or:

    pip install prowlarr-py

## Using this collection

You can either call modules by their Fully Qualified Collection Name (FQCN), such as `devopsarr.prowlarr.prowlarr_tag`, or you can call modules by their short name if you list the `devopsarr.prowlarr` collection in the playbook's `collections` keyword:

```yaml
---
  - name: Create tag with FQCN
    devopsarr.prowlarr.prowlarr_tag:
      label: example
      prowlarr_api_key: "{{ prowlarr_api_key }}"
      prowlarr_url: "{{ prowlarr_url }}"

---
  - name: Create tag with short name
    prowlarr_tag:
      label: example
      prowlarr_api_key: "{{ prowlarr_api_key }}"
      prowlarr_url: "{{ prowlarr_url }}"
```

## Release notes

See the [changelog](https://github.com/devopsarr/ansible-collection-prowlarr/tree/main/CHANGELOG.rst).

## More information

- [Ansible Collection overview](https://github.com/ansible-collections/overview)
- [Ansible User guide](https://docs.ansible.com/ansible/devel/user_guide/index.html)
- [Ansible Developer guide](https://docs.ansible.com/ansible/devel/dev_guide/index.html)
- [Ansible Collections Checklist](https://github.com/ansible-collections/overview/blob/main/collection_requirements.rst)
- [Ansible Community code of conduct](https://docs.ansible.com/ansible/devel/community/code_of_conduct.html)
- [The Bullhorn (the Ansible Contributor newsletter)](https://us19.campaign-archive.com/home/?u=56d874e027110e35dea0e03c1&id=d6635f5420)
- [News for Maintainers](https://github.com/ansible-collections/news-for-maintainers)

## Licensing

GNU General Public License v3.0 or later.

See [LICENSE](https://www.gnu.org/licenses/gpl-3.0.txt) to see the full text.
