#!/usr/bin/python

# Copyright: (c) 2020, Fuochi <devopsarr@gmail.com>
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)
from __future__ import (absolute_import, division, print_function)

__metaclass__ = type

DOCUMENTATION = r'''
---
module: prowlarr_application_info

short_description: Get information about Prowlarr application.

version_added: "1.0.0"

description: Get information about Prowlarr application.

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
# Gather information about all applications.
- name: Gather information about all applications
  devopsarr.prowlarr.prowlarr_application_info:

# Gather information about a single application.
- name: Gather information about a single application
  devopsarr.prowlarr.prowlarr_application_info:
    name: test
'''

RETURN = r'''
# These are examples of possible return values, and in general should use other names for return values.
applications:
    description: A list of applications.
    returned: always
    type: list
    elements: dict
    contains:
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


def list_applications(result):
    try:
        return client.list_applications()
    except prowlarr.ApiException as e:
        module.fail_json('Error listing applications: {}\n body: {}'.format(to_native(e.reason), to_native(e.body)), **result)
    except Exception as e:
        module.fail_json('Error listing applications: {}'.format(to_native(e)), **result)


def populate_applications(result):
    applications = []
    # Check if a resource is present already.
    for application in list_applications(result):
        if module.params['name']:
            if application.name == module.params['name']:
                applications = [application.model_dump(by_alias=False)]
        else:
            applications.append(application.model_dump(by_alias=False))
    return applications


def run_module():
    global client
    global module

    # Define available arguments/parameters a user can pass to the module
    module = ProwlarrModule(
        argument_spec=init_module_args(),
        supports_check_mode=True,
    )
    # Init client and result.
    client = prowlarr.ApplicationApi(module.api)
    result = dict(
        changed=False,
        applications=[],
    )

    # List resources.
    result.update(applications=populate_applications(result))

    # Exit with data.
    module.exit_json(**result)


def main():
    run_module()


if __name__ == '__main__':
    main()
