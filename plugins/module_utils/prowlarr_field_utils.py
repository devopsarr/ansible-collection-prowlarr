# Copyright: (c) 2020, Fuochi <devopsarr@gmail.com>
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)
from __future__ import (absolute_import, division, print_function)

__metaclass__ = type

try:
    import prowlarr
    HAS_PROWLARR_LIBRARY = True
except ImportError:
    HAS_PROWLARR_LIBRARY = False


class FieldHelper():
    def __init__(self):
        # type: () -> None
        self.field_args = dict(
            name=dict(type='str'),
            value=dict(type='raw'),
        )

    def populate_fields(self, field_list):
        # type: (list) -> list[prowlarr.ContractField]
        fields = []

        for field in field_list:
            fields.append(
                prowlarr.ContractField(
                    name=field['name'],
                    value=field['value'],
                ),
            )

        return fields
