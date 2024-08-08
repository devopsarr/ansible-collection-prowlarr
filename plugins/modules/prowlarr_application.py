#!/usr/bin/python

# Copyright: (c) 2020, Fuochi <devopsarr@gmail.com>
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)
from __future__ import (absolute_import, division, print_function)

__metaclass__ = type

DOCUMENTATION = r'''
---
module: prowlarr_application

short_description: Manages Prowlarr application.

version_added: "1.0.0"

description: Manages Prowlarr application.

options:
    name:
        description: Name.
        required: true
        type: str
    sync_level:
        description: Sync level.
        type: str
        default: fullSync
        choices: [ "fullSync", "addOnly", "disabled" ]
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
# Create a application
- name: Create a application
  devopsarr.prowlarr.prowlarr_application:
    name: Example
    sync_level: disabled
    config_contract: RadarrSettings
    implementation: Radarr
    fields:
      - name: prowlarrUrl
        value: http://localhost:9696
      - name: baseUrl
        value: http://localhost:967878
      - name: apiKey
        value: apiKey123
      - name: syncCategories
        value:
          - 2000
          - 2010
          - 2030
      - name: syncRejectBlocklistedTorrentHashesWhileGrabbing
        value: false
    tags: [1,2]

# Delete a application
- name: Delete a application
  devopsarr.prowlarr.prowlarr_application:
    name: Example
    state: absent
'''

RETURN = r'''
# These are examples of possible return values, and in general should use other names for return values.
id:
    description: application ID.
    type: int
    returned: always
    sample: 1
name:
    description: Name.
    returned: always
    type: str
    sample: "Example"
sync_level:
    description: Sync level.
    returned: always
    type: str
    sample: disabled
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
            want.sync_level != status.sync_level or
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
        sync_level=dict(type='str', default='fullSync', choices=['fullSync', 'addOnly', 'disabled']),
        config_contract=dict(type='str'),
        implementation=dict(type='str'),
        tags=dict(type='list', elements='int', default=[]),
        fields=dict(type='list', elements='dict', options=field_helper.field_args),
        state=dict(default='present', type='str', choices=['present', 'absent']),
        # Needed to manage obfuscate response from api "********"
        update_secrets=dict(type='bool', default=False),
    )


def create_application(want, result):
    result['changed'] = True
    # Only without check mode.
    if not module.check_mode:
        try:
            response = client.create_applications(application_resource=want)
        except prowlarr.ApiException as e:
            module.fail_json('Error creating application: {}\n body: {}'.format(to_native(e.reason), to_native(e.body)), **result)
        except Exception as e:
            module.fail_json('Error creating application: {}'.format(to_native(e)), **result)
        result.update(response.model_dump(by_alias=False))
    module.exit_json(**result)


def list_applications(result):
    try:
        return client.list_applications()
    except prowlarr.ApiException as e:
        module.fail_json('Error listing applications: {}\n body: {}'.format(to_native(e.reason), to_native(e.body)), **result)
    except Exception as e:
        module.fail_json('Error listing applications: {}'.format(to_native(e)), **result)


def find_application(name, result):
    for application in list_applications(result):
        if application.name == name:
            return application
    return None


def update_application(want, result):
    result['changed'] = True
    # Only without check mode.
    if not module.check_mode:
        try:
            response = client.update_applications(application_resource=want, id=str(want.id))
        except prowlarr.ApiException as e:
            module.fail_json('Error updating application: {}\n body: {}'.format(to_native(e.reason), to_native(e.body)), **result)
        except Exception as e:
            module.fail_json('Error updating application: {}'.format(to_native(e)), **result)
    # No need to exit module since it will exit by default either way
    result.update(response.model_dump(by_alias=False))


def delete_application(result):
    if result['id'] != 0:
        result['changed'] = True
        if not module.check_mode:
            try:
                client.delete_applications(result['id'])
            except prowlarr.ApiException as e:
                module.fail_json('Error deleting application: {}\n body: {}'.format(to_native(e.reason), to_native(e.body)), **result)
            except Exception as e:
                module.fail_json('Error deleting application: {}'.format(to_native(e)), **result)
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
    client = prowlarr.ApplicationApi(module.api)
    result = dict(
        changed=False,
        id=0,
    )

    # Check if a resource is present already.
    state = find_application(module.params['name'], result)
    if state:
        result.update(state.model_dump(by_alias=False))

    # Delete the resource if needed.
    if module.params['state'] == 'absent':
        delete_application(result)

    # Set wanted resource.
    want = prowlarr.ApplicationResource(
        name=module.params['name'],
        sync_level=module.params['sync_level'],
        config_contract=module.params['config_contract'],
        implementation=module.params['implementation'],
        tags=module.params['tags'],
        fields=field_helper.populate_fields(module.params['fields']),
    )

    # Create a new resource if needed.
    if result['id'] == 0:
        create_application(want, result)

    # Update an existing resource.
    want.id = result['id']
    if is_changed(state, want) or module.params['update_secrets']:
        update_application(want, result)

    # Exit whith no changes.
    module.exit_json(**result)


def main():
    run_module()


if __name__ == '__main__':
    main()
