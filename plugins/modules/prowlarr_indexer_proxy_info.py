#!/usr/bin/python

# Copyright: (c) 2020, Fuochi <devopsarr@gmail.com>
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)
from __future__ import (absolute_import, division, print_function)

__metaclass__ = type

DOCUMENTATION = r'''
---
module: prowlarr_indexer_proxy_info

short_description: Get information about Prowlarr indexer proxy.

version_added: "1.0.0"

description: Get information about Prowlarr indexer proxy.

options:
    name:
        description: Name.
        type: str

extends_documentation_fragment:
    - devopsarr.prowlarr.prowlarr_credentials

author:
    - Fuochi (@Fuochi)
'''

EXAMPLES = r'''
---
# Gather information about all indexer proxies.
- name: Gather information about all indexer proxies
  devopsarr.prowlarr.prowlarr_indexer_proxy_info:

# Gather information about a single indexer proxy.
- name: Gather information about a single indexer proxy
  devopsarr.prowlarr.prowlarr_indexer_proxy_info:
    name: test
'''

RETURN = r'''
# These are examples of possible return values, and in general should use other names for return values.
indexer_proxies:
    description: A list of indexer_proxies.
    returned: always
    type: list
    elements: dict
    contains:
        id:
            description: Indexer proxy ID.
            type: int
            returned: always
            sample: 1
        name:
            description: Name.
            returned: always
            type: str
            sample: "Example"
        config_contract:
            description: Config contract.
            returned: always
            type: str
            sample: "WebhookSettings"
        implementation:
            description: Implementation.
            returned: always
            type: str
            sample: "Webhook"
        tags:
            description: Tag list.
            type: list
            returned: always
            elements: int
            sample: [1,2]
        fields:
            description: field list.
            type: list
            returned: always
'''

from ansible_collections.devopsarr.prowlarr.plugins.module_utils.prowlarr_module import ProwlarrModule
from ansible.module_utils.common.text.converters import to_native

try:
    import prowlarr
    HAS_PROWLARR_LIBRARY = True
except ImportError:
    HAS_PROWLARR_LIBRARY = False


def init_module_args():
    # define available arguments/parameters a user can pass to the module
    return dict(
        name=dict(type='str'),
    )


def list_indexer_proxies(result):
    try:
        return client.list_indexer_proxy()
    except prowlarr.ApiException as e:
        module.fail_json('Error listing indexer proxies: {}\n body: {}'.format(to_native(e.reason), to_native(e.body)), **result)
    except Exception as e:
        module.fail_json('Error listing indexer proxies: {}'.format(to_native(e)), **result)


def populate_indexer_proxies(result):
    indexer_proxies = []
    # Check if a resource is present already.
    for indexer_proxy in list_indexer_proxies(result):
        if module.params['name']:
            if indexer_proxy.name == module.params['name']:
                indexer_proxies = [indexer_proxy.model_dump(by_alias=False)]
        else:
            indexer_proxies.append(indexer_proxy.model_dump(by_alias=False))
    return indexer_proxies


def run_module():
    global client
    global module

    # Define available arguments/parameters a user can pass to the module
    module = ProwlarrModule(
        argument_spec=init_module_args(),
        supports_check_mode=True,
    )
    # Init client and result.
    client = prowlarr.IndexerProxyApi(module.api)
    result = dict(
        changed=False,
        indexer_proxies=[],
    )

    # List resources.
    result.update(indexer_proxies=populate_indexer_proxies(result))

    # Exit with data.
    module.exit_json(**result)


def main():
    run_module()


if __name__ == '__main__':
    main()
