#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: (c) 2020, Josh Williams <vmizzle@gmail.com>
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

ANSIBLE_METADATA = {'metadata_version': '1.1',
                    'status': ['preview'],
                    'supported_by': 'community'}

DOCUMENTATION = r'''
---
module: nextcloud_setting
short_description: Configures Nextcloud (via occ config:set)
description:
    - This module updates Nextcloud settings via C(occ config:set) or C(occ config:import)
options:
    name:
        required: true
        description:
            - Name of the setting being updated/removed
    type:
        required: true
        choices: ["system", "app"]
        description:
            - Type of setting (app or system)
    appname:
        required: false
        description:
            - Name of the app being configured (for I(type) = C(app))
    value:
        description:
            - New value.
    state:
        choices: ["present", "absent"]
        default: "present"
        description:
            - Desired setting state
    nextcloud_root:
        required: true
        description:
            - Nextcloud root directory
'''

EXAMPLES = r'''
- name: ensure the external url is configured
  nextcloud_setting:
    name: overwrite.cli.url
    type: system
    value: https://example.com
    nextcloud_root: /opt/nextcloud/
  become: yes
  become_user: www-data
  become_method: sudo

- name: ensure Nextcloud uses Redis for distributed caching
  nextcloud_setting:
    name: "{{ item.name }}"
    type: system
    value: "{{ item.value }}"
    nextcloud_root: /opt/nextcloud/
  loop:
    - name: memcache.distributed
      type: system
      value: "\\OC\\Memcache\\Redis"
    - name: redis
      type: system
      value:
        host: /var/run/redis/redis.sock
        port: 0
        timeput: 0.0
  become: yes
  become_user: www-data
  become_method: sudo
'''
from ansible.module_utils.basic import AnsibleModule
from ansible.module_utils.six import text_type, string_types
import json
import tempfile
import os

class NextcloudSetting(object):
    def __init__(self, module):
        self.module         = module
        self.state          = module.params['state']
        self.type           = module.params['type']
        self.appname        = module.params['appname']
        self.name           = module.params['name']
        self.value          = module.params['value']
        self.nextcloud_root = module.params['nextcloud_root']

        self._settings      = None

    def _exec_cmd(self, cmd):
        return self.module.run_command(cmd, cwd=self.nextcloud_root)

    def _all_settings(self):
        if self._settings is not None:
            return self._settings

        (rc, out, err) = self._exec_cmd(
                'php occ config:list --private --output json')

        if rc != 0:
                self.module.fail_json(
                        name=self.name,
                        msg='Error getting settings list.',
                        rc=rc,
                        err=err)

        self._settings = json.loads(out)
        return self._settings

    def _is_present(self):
        settings = self._all_settings()

        if self.type == 'system' and self.name in settings['system']:
            return True
        elif self.type == 'app' and self.name in settings['apps'][self.appname]:
            return True
        else:
            return False

    def _current_value(self):
        if not self._is_present():
            return None

        settings = self._all_settings()

        if self.type == 'system':
            return settings['system'][self.name]
        elif self.type == 'app':
            return settings['apps'][self.appname][self.name]

    def update(self):
        current = self._current_value()

        thecmd = None
        if current == self.value:
            return (False, '', '')
        else:
            if isinstance(self.value, string_types):
                if self.type == 'system':
                    thecmd = 'php occ config:system:set %s --value="%s"' % (self.name, self.value)
                elif self.type == 'app':
                    thecmd = 'php occ config:app:set %s %s --value="%s"' % (self.appname, self.name, self.value)
            else:
                d = dict(system=dict(), apps=dict())
                if self.type == 'system':
                    d['system'][self.name] = self.value
                elif self.type == 'app':
                    d['apps'][self.appname] = dict()
                    d['apps'][self.appname][self.name] = self.value

                handle, filename = tempfile.mkstemp(prefix='nextcloud_setting')
                with os.fdopen(handle, "w") as f:
                    json.dump(d, f)
                    f.close()

                thecmd = 'php occ config:import %s' % filename

            (rc, out, err) = self._exec_cmd(thecmd)
            if rc != 0:
                self.module.fail_json(msg='Error updating setting.', rc=rc, err=err)

            self._settngs = None

            return (True, out, err)

    def remove(self):
        if not self._is_present():
            return (False, '', '')

        thecmd = None
        if self.type == 'system':
            thecmd = 'php occ config:system:delete %s' % self.name
        elif self.type == 'app':
            thecmd = 'php occ config:app:delete %s %s' % (self.appname, self.name)

        (rc, out, err) = self._exec_cmd(thecmd)
        if rc != 0:
            self.module.fail_json(msg='Error removing setting.', rc=rc, err=err)

        self._settings = None

        return (True, out, err)

def main():
    module = AnsibleModule(
        argument_spec=dict(
            name=dict(type='str', required=True),
            state=dict(type='str', default='present', choices=['absent', 'present']),
            type=dict(type='str', default='system', choices=['system', 'app']),
            value=dict(type='raw', aliases=['values']),
            appname=dict(type='str'),
            nextcloud_root=dict(type='str', required=True),
        ),
        supports_check_mode=True,
        required_if=(
            ['type', 'app', ['appname']],
            ['state', 'present', ['value']]
        )
    )

    if module.params['name'] is None:
        module.fail_json(msg='name cannot be None')

    setting = NextcloudSetting(module)

    changed = False
    result = {}
    result['name']  = setting.name
    result['state'] = setting.state
    result['type']  = setting.type

    if setting.state == 'absent':
        (changed, out, err) = setting.remove()
    else:
        (changed, out, err) = setting.update()

    result['changed'] = changed

    if out:
        result['stdout'] = out
    if err:
        result['stderr'] = err

    module.exit_json(**result)

if __name__ == '__main__':
    main()
