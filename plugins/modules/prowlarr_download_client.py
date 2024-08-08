#!/usr/bin/python

# Copyright: (c) 2020, Fuochi <devopsarr@gmail.com>
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)
from __future__ import (absolute_import, division, print_function)

__metaclass__ = type

DOCUMENTATION = r'''
---
module: prowlarr_download_client

short_description: Manages Prowlarr download client.

version_added: "1.0.0"

description: Manages Prowlarr download client.

options:
    name:
        description: Name.
        required: true
        type: str
    enable:
        description: Enable flag.
        type: bool
    priority:
        description: Priority.
        type: int
    protocol:
        description: Protocol.
        choices: [ "torrent", "usenet" ]
        type: str
    categories:
        description: List of mapped categories.
        type: list
        elements: dict
        default: []
        suboptions:
            client_category:
                description: Client category name.
                type: str
            categories:
                description: Mapped category list.
                type: list
                elements: int
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
# Create a download client
- name: Create a download client
  devopsarr.prowlarr.prowlarr_download_client:
    enable: false
    priority: 1
    name: "Hadouken"
    fields:
    - name: "host"
      value: "hadouken.lcl"
    - name: "urlBase"
      value: "/hadouken/"
    - name: "port"
      value: 9091
    - name: "category"
      value: "prowlarr-tv"
    - name: "username"
      value: "username"
    - name: "password"
      value: "password"
    - name: "useSsl"
      value: true
    protocol: "torrent"
    config_contract: "HadoukenSettings"
    implementation: "Hadouken"
    tags: [1,2]

# Delete a download client
- name: Delete a download client
  devopsarr.prowlarr.prowlarr_download_client:
    name: Example
    state: absent
'''

RETURN = r'''
# These are examples of possible return values, and in general should use other names for return values.
id:
    description: download clientID.
    type: int
    returned: always
    sample: 1
name:
    description: Name.
    returned: always
    type: str
    sample: "Example"
enable:
    description: Enable flag.
    returned: always
    type: bool
    sample: true
priority:
    description: Priority.
    returned: always
    type: int
    sample: 1
config_contract:
    description: Config contract.
    returned: always
    type: str
    sample: "BroadcastheNetSettings"
implementation:
    description: Implementation.
    returned: always
    type: str
    sample: "BroadcastheNet"
protocol:
    description: Protocol.
    returned: always
    type: str
    sample: "torrent"
categories:
    description: List of mapped categories.
    type: list
    elements: dict
    returned: always
    sample:
      - client_category: "example"
        categories: [0]
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
            want.enable != status.enable or
            want.priority != status.priority or
            want.config_contract != status.config_contract or
            want.implementation != status.implementation or
            want.protocol != status.protocol or
            len(want.categories) != len(status.categories) or
            want.tags != status.tags):
        return True

    for status_category in status.categories:
        for want_category in want.categories:
            if want_category.client_category == status_category.client_category and want_category.categories != status_category.categories:
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
        enable=dict(type='bool'),
        priority=dict(type='int'),
        config_contract=dict(type='str'),
        implementation=dict(type='str'),
        protocol=dict(type='str', choices=['usenet', 'torrent']),
        categories=dict(type='list', elements='dict', default=[]),
        tags=dict(type='list', elements='int', default=[]),
        fields=dict(type='list', elements='dict', options=field_helper.field_args),
        state=dict(default='present', type='str', choices=['present', 'absent']),
        # Needed to manage obfuscate response from api "********"
        update_secrets=dict(type='bool', default=False),
    )


def create_download_client(want, result):
    result['changed'] = True
    # Only without check mode.
    if not module.check_mode:
        try:
            response = client.create_download_client(download_client_resource=want)
        except prowlarr.ApiException as e:
            module.fail_json('Error creating download client: {}\n body: {}'.format(to_native(e.reason), to_native(e.body)), **result)
        except Exception as e:
            module.fail_json('Error creating download client: {}'.format(to_native(e)), **result)
        result.update(response.model_dump(by_alias=False))
    module.exit_json(**result)


def list_download_clients(result):
    try:
        return client.list_download_client()
    except prowlarr.ApiException as e:
        module.fail_json('Error listing download clients: {}\n body: {}'.format(to_native(e.reason), to_native(e.body)), **result)
    except Exception as e:
        module.fail_json('Error listing download clients: {}'.format(to_native(e)), **result)


def find_download_client(name, result):
    for download_client in list_download_clients(result):
        if download_client.name == name:
            return download_client
    return None


def update_download_client(want, result):
    result['changed'] = True
    # Only without check mode.
    if not module.check_mode:
        try:
            response = client.update_download_client(download_client_resource=want, id=str(want.id))
        except prowlarr.ApiException as e:
            module.fail_json('Error updating download client: {}\n body: {}'.format(to_native(e.reason), to_native(e.body)), **result)
        except Exception as e:
            module.fail_json('Error updating download client: {}'.format(to_native(e)), **result)
    # No need to exit module since it will exit by default either way
    result.update(response.model_dump(by_alias=False))


def delete_download_client(result):
    if result['id'] != 0:
        result['changed'] = True
        if not module.check_mode:
            try:
                client.delete_download_client(result['id'])
            except prowlarr.ApiException as e:
                module.fail_json('Error deleting download client: {}\n body: {}'.format(to_native(e.reason), to_native(e.body)), **result)
            except Exception as e:
                module.fail_json('Error deleting download client: {}'.format(to_native(e)), **result)
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
    client = prowlarr.DownloadClientApi(module.api)
    result = dict(
        changed=False,
        id=0,
    )

    # Check if a resource is present already.
    state = find_download_client(module.params['name'], result)
    if state:
        result.update(state.model_dump(by_alias=False))

    # Delete the resource if needed.
    if module.params['state'] == 'absent':
        delete_download_client(result)

    # Set wanted resource.
    want = prowlarr.DownloadClientResource(
        name=module.params['name'],
        enable=module.params['enable'],
        priority=module.params['priority'],
        config_contract=module.params['config_contract'],
        implementation=module.params['implementation'],
        protocol=module.params['protocol'],
        categories=module.params['categories'],
        tags=module.params['tags'],
        fields=field_helper.populate_fields(module.params['fields']),
    )

    # Create a new resource, if needed.
    if result['id'] == 0:
        create_download_client(want, result)

    # Update an existing resource.
    want.id = result['id']
    if is_changed(state, want) or module.params['update_secrets']:
        update_download_client(want, result)

    # Exit whith no changes.
    module.exit_json(**result)


def main():
    run_module()


if __name__ == '__main__':
    main()
