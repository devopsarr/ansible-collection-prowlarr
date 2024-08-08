#!/usr/bin/python

# Copyright: (c) 2020, Fuochi <devopsarr@gmail.com>
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)
from __future__ import (absolute_import, division, print_function)

__metaclass__ = type

DOCUMENTATION = r'''
---
module: prowlarr_indexer_proxy

short_description: Manages Prowlarr indexer proxy.

version_added: "1.0.0"

description: Manages Prowlarr indexer proxy.

options:
    name:
        description: Name.
        required: true
        type: str
    update_secrets:
        description: Flag to force update of secret fields.
        type: bool
        default: false

extends_documentation_fragment:
    - devopsarr.prowlarr.prowlarr_credentials
    - devopsarr.prowlarr.prowlarr_implementation
    - devopsarr.prowlarr.prowlarr_taggable
    - devopsarr.prowlarr.prowlarr_state

author:
    - Fuochi (@Fuochi)
'''

EXAMPLES = r'''
---
# Create a indexer proxy
- name: Create a indexer proxy
  devopsarr.prowlarr.prowlarr_indexer_proxy:
    name: Example
    config_contract: FlareSolverrSettings
    implementation: FlareSolverr
    fields:
      - name: host
        value: http://localhost:8191
      - name: requestTimeout
        value: 60
    tags: [1,2]

# Delete a indexer proxy
- name: Delete a indexer proxy
  devopsarr.prowlarr.prowlarr_indexer_proxy:
    name: Example
    state: absent
'''

RETURN = r'''
# These are examples of possible return values, and in general should use other names for return values.
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
from ansible_collections.devopsarr.prowlarr.plugins.module_utils.prowlarr_field_utils import FieldHelper
from ansible.module_utils.common.text.converters import to_native

try:
    import prowlarr
    HAS_PROWLARR_LIBRARY = True
except ImportError:
    HAS_PROWLARR_LIBRARY = False


def is_changed(status, want):
    if (want.name != status.name or
            want.config_contract != status.config_contract or
            want.implementation != status.implementation or
            want.tags != status.tags):
        return True

    for status_field in status.fields:
        for want_field in want.fields:
            if want_field.name == status_field.name and want_field.value != status_field.value and status_field.value != "********":
                return True
    return False


def init_module_args():
    # define available arguments/parameters a user can pass to the module
    return dict(
        name=dict(type='str', required=True),
        config_contract=dict(type='str'),
        implementation=dict(type='str'),
        tags=dict(type='list', elements='int', default=[]),
        fields=dict(type='list', elements='dict', options=field_helper.field_args),
        state=dict(default='present', type='str', choices=['present', 'absent']),
        # Needed to manage obfuscate response from api "********"
        update_secrets=dict(type='bool', default=False),
    )


def create_indexer_proxy(want, result):
    result['changed'] = True
    # Only without check mode.
    if not module.check_mode:
        try:
            response = client.create_indexer_proxy(indexer_proxy_resource=want)
        except prowlarr.ApiException as e:
            module.fail_json('Error creating indexer proxy: {}\n body: {}'.format(to_native(e.reason), to_native(e.body)), **result)
        except Exception as e:
            module.fail_json('Error creating indexer proxy: {}'.format(to_native(e)), **result)
        result.update(response.model_dump(by_alias=False))
    module.exit_json(**result)


def list_indexer_proxies(result):
    try:
        return client.list_indexer_proxy()
    except prowlarr.ApiException as e:
        module.fail_json('Error listing indexer proxies: {}\n body: {}'.format(to_native(e.reason), to_native(e.body)), **result)
    except Exception as e:
        module.fail_json('Error listing indexer proxies: {}'.format(to_native(e)), **result)


def find_indexer_proxy(name, result):
    for indexer_proxy in list_indexer_proxies(result):
        if indexer_proxy.name == name:
            return indexer_proxy
    return None


def update_indexer_proxy(want, result):
    result['changed'] = True
    # Only without check mode.
    if not module.check_mode:
        try:
            response = client.update_indexer_proxy(indexer_proxy_resource=want, id=str(want.id))
        except prowlarr.ApiException as e:
            module.fail_json('Error updating indexer proxy: {}\n body: {}'.format(to_native(e.reason), to_native(e.body)), **result)
        except Exception as e:
            module.fail_json('Error updating indexer proxy: {}'.format(to_native(e)), **result)
    # No need to exit module since it will exit by default either way
    result.update(response.model_dump(by_alias=False))


def delete_indexer_proxy(result):
    if result['id'] != 0:
        result['changed'] = True
        if not module.check_mode:
            try:
                client.delete_indexer_proxy(result['id'])
            except prowlarr.ApiException as e:
                module.fail_json('Error deleting indexer proxy: {}\n body: {}'.format(to_native(e.reason), to_native(e.body)), **result)
            except Exception as e:
                module.fail_json('Error deleting indexer proxy: {}'.format(to_native(e)), **result)
            result['id'] = 0
    module.exit_json(**result)


def run_module():
    global client
    global module
    global field_helper

    # Init helper.
    field_helper = FieldHelper()

    # Define available arguments/parameters a user can pass to the module
    module = ProwlarrModule(
        argument_spec=init_module_args(),
        supports_check_mode=True,
    )

    # Init client and result.
    client = prowlarr.IndexerProxyApi(module.api)
    result = dict(
        changed=False,
        id=0,
    )

    # Check if a resource is present already.
    state = find_indexer_proxy(module.params['name'], result)
    if state:
        result.update(state.model_dump(by_alias=False))

    # Delete the resource if needed.
    if module.params['state'] == 'absent':
        delete_indexer_proxy(result)

    # Set wanted resource.
    want = prowlarr.IndexerProxyResource(
        name=module.params['name'],
        config_contract=module.params['config_contract'],
        implementation=module.params['implementation'],
        tags=module.params['tags'],
        fields=field_helper.populate_fields(module.params['fields']),
    )

    # Create a new resource if needed.
    if result['id'] == 0:
        create_indexer_proxy(want, result)

    # Update an existing resource.
    want.id = result['id']
    if is_changed(state, want) or module.params['update_secrets']:
        update_indexer_proxy(want, result)

    # Exit whith no changes.
    module.exit_json(**result)


def main():
    run_module()


if __name__ == '__main__':
    main()
