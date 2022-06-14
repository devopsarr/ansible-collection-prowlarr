# Copyright: (c) 2020, Fuochi <devopsarr@gmail.com>
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)
from __future__ import (absolute_import, division, print_function)
__metaclass__ = type


class ModuleDocFragment(object):

    # Plugin options for Prowlarr credentials
    DOCUMENTATION = r'''
options:
  prowlarr_url:
    description: Full Prowlarr URL with protocol and port (e.g. `https://test.prowlarr.tv:9696`)
    type: str
    required: true
  prowlarr_api_key:
    description: API key for Prowlarr authentication.
    type: str
    required: true
notes:
  - for authentication, you can set service_account_file using the c(SONARR_URL) env variable.
  - for authentication, you can set service_account_contents using the c(SONARR_API_KEY) env variable.
'''
