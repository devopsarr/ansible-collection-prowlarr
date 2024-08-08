#!/usr/bin/python

# Copyright: (c) 2020, Fuochi <devopsarr@gmail.com>
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)
from __future__ import (absolute_import, division, print_function)

__metaclass__ = type

DOCUMENTATION = r'''
---
module: prowlarr_sync_profile_info

short_description: Get information about Prowlarr sync profile.

version_added: "1.0.0"

description: Get information about Prowlarr sync profile.

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
# Gather information about all sync profiles.
- name: Gather information about all sync profiles
  devopsarr.prowlarr.prowlarr_sync_profile_info:

# Gather information about a single sync profile.
- name: Gather information about a single sync profile
  devopsarr.prowlarr.prowlarr_sync_profile_info:
    name: test
'''

RETURN = r'''
# These are examples of possible return values, and in general should use other names for return values.
sync_profiles:
    description: A list of sync profiles.
    returned: always
    type: list
    elements: dict
    contains:
        id:
            description: Sync Profile ID.
            type: int
            returned: always
            sample: 1
        enable_automatic_search:
            description: Enable automatic search.
            type: bool
            returned: always
            sample: True
        enable_interactive_search:
            description: Enable interactive search.
            type: bool
            returned: always
            sample: True
        minimum_seeders:
            description: Indexer ID. Set `0` for all."
            type: int
            returned: always
            sample: 1
        enable_rss:
            description: Enable rss.
            type: bool
            returned: always
            sample: True
        tags:
            description: Tag list.
            type: list
            returned: always
            elements: int
            sample: [1,2]
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


def list_sync_profile(result):
    try:
        return client.list_app_profile()
    except prowlarr.ApiException as e:
        module.fail_json('Error listing sync profiles: {}\n body: {}'.format(to_native(e.reason), to_native(e.body)), **result)
    except Exception as e:
        module.fail_json('Error listing sync profiles: {}'.format(to_native(e)), **result)


def populate_sync_profile(result):
    profiles = []
    # Check if a resource is present already.
    for profile in list_sync_profile(result):
        if module.params['name']:
            if profile.name == module.params['name']:
                profiles = [profile.model_dump(by_alias=False)]
        else:
            profiles.append(profile.model_dump(by_alias=False))
    return profiles


def run_module():
    global client
    global module

    # Define available arguments/parameters a user can pass to the module
    module = ProwlarrModule(
        argument_spec=init_module_args(),
        supports_check_mode=True,
    )
    # Init client and result.
    client = prowlarr.AppProfileApi(module.api)
    result = dict(
        changed=False,
        sync_profiles=[],
    )

    # List resources.
    result.update(sync_profiles=populate_sync_profile(result))

    # Exit with data.
    module.exit_json(**result)


def main():
    run_module()


if __name__ == '__main__':
    main()
