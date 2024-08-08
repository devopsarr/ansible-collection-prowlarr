#!/usr/bin/python

# Copyright: (c) 2020, Fuochi <devopsarr@gmail.com>
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)
from __future__ import (absolute_import, division, print_function)

__metaclass__ = type

DOCUMENTATION = r'''
---
module: prowlarr_application_schema_info

short_description: Get information about Prowlarr application schema.

version_added: "1.0.0"

description: Get information about Prowlarr application schema.

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
# Gather information about all applications schema.
- name: Gather information about all applications schema
  devopsarr.prowlarr.prowlarr_application_schema_info:

# Gather information about a single application schema.
- name: Gather information about a single application schema
  devopsarr.prowlarr.prowlarr_application_schema_info:
    name: BroadcastheNet
'''

RETURN = r'''
# These are examples of possible return values, and in general should use other names for return values.
applications:
    description: A list of applications schema.
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
        enable_automatic_search:
            description: Enable automatic search flag.
            returned: always
            type: bool
            sample: true
        enable_interactive_search:
            description: Enable interactive search flag.
            returned: always
            type: bool
            sample: false
        enable_rss:
            description: Enable RSS flag.
            returned: always
            type: bool
            sample: true
        priority:
            description: Priority.
            returned: always
            type: int
            sample: 1
        download_client_id:
            description: Download client ID.
            returned: always
            type: int
            sample: 0
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


def list_application_schema(result):
    try:
        return client.list_applications_schema()
    except prowlarr.ApiException as e:
        module.fail_json('Error listing application schemas: {}\n body: {}'.format(to_native(e.reason), to_native(e.body)), **result)
    except Exception as e:
        module.fail_json('Error listing application schemas: {}'.format(to_native(e)), **result)


def populate_application_schema(result):
    applications = []
    # Check if a resource is present already.
    for application in list_application_schema(result):
        if module.params['name']:
            if application.implementation == module.params['name']:
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
    result.update(applications=populate_application_schema(result))

    # Exit with data.
    module.exit_json(**result)


def main():
    run_module()


if __name__ == '__main__':
    main()
