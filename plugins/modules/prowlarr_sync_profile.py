#!/usr/bin/python

# Copyright: (c) 2020, Fuochi <devopsarr@gmail.com>
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)
from __future__ import (absolute_import, division, print_function)

__metaclass__ = type

DOCUMENTATION = r'''
---
module: prowlarr_sync_profile

short_description: Manages Prowlarr sync profile.

version_added: "1.0.0"

description: Manages Prowlarr sync profile.

options:
    name:
        description: Name.
        required: true
        type: str
    enable_interactive_search:
        description: Enable interactive search.
        type: bool
    enable_automatic_search:
        description: Enable automatic search.
        type: bool
    enable_rss:
        description: Enable RSS.
        type: bool
    minimum_seeders:
        description: Minimum seeders.
        type: int

extends_documentation_fragment:
    - devopsarr.prowlarr.prowlarr_credentials
    - devopsarr.prowlarr.prowlarr_taggable
    - devopsarr.prowlarr.prowlarr_state

author:
    - Fuochi (@Fuochi)
'''

EXAMPLES = r'''
---
# Create a sync profile
- name: Create a sync profile
  devopsarr.prowlarr.prowlarr_sync_profile:
    name: "Example"
    enable_rss: true
    enable_interactive_search: false
    enable_automatic_search: true
    minimum_seeders: 1
    tags: [1,2]

# Delete a sync profile
- name: Delete a sync_profile
  devopsarr.prowlarr.prowlarr_sync_profile:
    name: Example
    state: absent
'''

RETURN = r'''
# These are examples of possible return values, and in general should use other names for return values.
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
        name=dict(type='str', required=True),
        enable_automatic_search=dict(type='bool'),
        enable_interactive_search=dict(type='bool'),
        minimum_seeders=dict(type='int'),
        enable_rss=dict(type='bool'),
        tags=dict(type='list', elements='int', default=[]),
        state=dict(default='present', type='str', choices=['present', 'absent']),
    )


def create_sync_profile(want, result):
    result['changed'] = True
    # Only without check mode.
    if not module.check_mode:
        try:
            response = client.create_app_profile(app_profile_resource=want)
        except prowlarr.ApiException as e:
            module.fail_json('Error creating sync profile: {}\n body: {}'.format(to_native(e.reason), to_native(e.body)), **result)
        except Exception as e:
            module.fail_json('Error creating sync profile: {}'.format(to_native(e)), **result)
        result.update(response.model_dump(by_alias=False))
    module.exit_json(**result)


def list_sync_profiles(result):
    try:
        return client.list_app_profile()
    except prowlarr.ApiException as e:
        module.fail_json('Error listing sync profiles: {}\n body: {}'.format(to_native(e.reason), to_native(e.body)), **result)
    except Exception as e:
        module.fail_json('Error listing sync profiles: {}'.format(to_native(e)), **result)


def find_sync_profile(name, result):
    for profile in list_sync_profiles(result):
        if profile.name == name:
            return profile
    return None


def update_sync_profile(want, result):
    result['changed'] = True
    # Only without check mode.
    if not module.check_mode:
        try:
            response = client.update_app_profile(app_profile_resource=want, id=str(want.id))
        except prowlarr.ApiException as e:
            module.fail_json('Error updating sync profile: {}\n body: {}'.format(to_native(e.reason), to_native(e.body)), **result)
        except Exception as e:
            module.fail_json('Error updating sync profile: {}'.format(to_native(e)), **result)
    # No need to exit module since it will exit by default either way
    result.update(response.model_dump(by_alias=False))


def delete_sync_profile(result):
    if result['id'] != 0:
        result['changed'] = True
        if not module.check_mode:
            try:
                client.delete_app_profile(result['id'])
            except prowlarr.ApiException as e:
                module.fail_json('Error deleting sync profile: {}\n body: {}'.format(to_native(e.reason), to_native(e.body)), **result)
            except Exception as e:
                module.fail_json('Error deleting sync profile: {}'.format(to_native(e)), **result)
            result['id'] = 0
    module.exit_json(**result)


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
        id=0,
    )

    # Check if a resource is present already.
    state = find_sync_profile(module.params['name'], result)
    if state:
        result.update(state.model_dump(by_alias=False))

    # Delete the resource if needed.
    if module.params['state'] == 'absent':
        delete_sync_profile(result)

    # Set wanted resource.
    want = prowlarr.AppProfileResource(
        name=module.params['name'],
        enable_rss=module.params['enable_rss'],
        enable_interactive_search=module.params['enable_interactive_search'],
        enable_automatic_search=module.params['enable_automatic_search'],
        minimum_seeders=module.params['minimum_seeders'],
        tags=module.params['tags'],
    )

    # Create a new resource if needed.
    if result['id'] == 0:
        create_sync_profile(want, result)

    # Update an existing resource.
    want.id = result['id']
    if want != state:
        update_sync_profile(want, result)

    # Exit whith no changes.
    module.exit_json(**result)


def main():
    run_module()


if __name__ == '__main__':
    main()
