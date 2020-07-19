#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: (c) 2019, Josh Williams <vmizzle@gmail.com>
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

ANSIBLE_METADATA = {'metadata_version': '1.1',
                    'status': ['preview'],
                    'supported_by': 'community'}

DOCUMENTATION = r'''
---
module: nextcloud_app
short_description: Adds (or removes) Nextcloud apps.
description:
    - Adds, removes, enables and disables apps in Nextcloud.

options:
    name:
        required: true
        description:
            - Name of the app to be installed/removed
    state:
        choices: ['present', 'absent']
        default: 'present'
        description:
            - Whether the app should be present or absent.
    enabled:
        choices: ['yes', 'no']
        default: 'yes'
        description:
            - Whether or not the app should be enabled within Nextcloud
    nextcloud_root:
        required: true
        description:
            - Nextcloud root directory
'''

from ansible.module_utils.basic import AnsibleModule
import json

class NextcloudApp(object):
    def __init__(self, module):
        self.module         = module
        self.name           = module.params['name']
        self.state          = module.params['state']
        self.enabled        = module.params['enabled']
        self.nextcloud_root = module.params['nextcloud_root']

        self._apps          = None

    def _exec_cmd(self, cmd):
        return self.module.run_command(cmd, cwd=self.nextcloud_root)

    def _all_apps(self):
        if self._apps is not None:
            return self._apps

        (rc, out, err) = self._exec_cmd("php occ app:list --output=json")
        if rc != 0:
            self.module.fail_json(
                    name=self.name,
                    msg='Error getting app list.',
                    rc=rc,
                    err=err)

        self._apps = json.loads(out)
        return self._apps

    def _is_installed(self):
        apps = self._all_apps()
        return ((self.name in apps['enabled']) or (self.name in apps['disabled']))

    def _is_enabled(self):
        if self._is_installed():
            apps = self._all_apps()
            return self.name in apps['enabled']
        else:
            return False

    def install(self):
        if self._is_installed():
            return (False, '', '')
        else:
            thecmd = "php occ app:install -vvv %s" % self.name
            (rc, out, err) = self._exec_cmd(thecmd)
            if rc != 0:
                self.module.fail_json(
                        name=self.name,
                        msg='Error installing app.',
                        rc=rc,
                        err=err)

            return (True, out, err)

    def remove(self):
        if self._is_installed():
            thecmd = "php occ app:remove %s" % self.name
            (rc, out, err) = self._exec_cmd(thecmd)
            if rc != 0:
                self.module.fail_json(
                        name=self.name,
                        msg='Error removing app.',
                        rc=rc,
                        err=err)

            return (True, out, err)
        else:
            return (False, '', '')

    def enable(self):
        if self._is_enabled():
            return (False, '', '')
        else:
            thecmd = "php occ app:enable %s" % self.name
            (rc, out, err) = self._exec_cmd(thecmd)
            if rc != 0:
                self.module.fail_json(
                        name=self.name,
                        msg='Error enabling app.',
                        rc=rc,
                        err=err)

            return (True, out, err)

    def disable(self):
        if self._is_enabled():
            thecmd = "php occ app:disable %s" % self.name
            (rc, out, err) = self._exec_cmd(thecmd)
            if rc != 0:
                self.module.fail_json(
                        name=self.name,
                        msg='Error disabling app.',
                        rc=rc,
                        err=err)

            return (True, out, err)
        else:
            return (False, '', '')

def main():
    module = AnsibleModule(
        argument_spec=dict(
            name=dict(type='str', required=True),
            state=dict(type='str', default='present', choices=['absent', 'present']),
            enabled=dict(type='bool', default=True),
            nextcloud_root=dict(type='str', required=True),
        ),
        supports_check_mode=True,
    )

    app = NextcloudApp(module)

    result = {}
    installed = False
    enabled = False
    out = ''
    err = ''

    result['name'] = app.name
    result['state'] = app.state
    result['enabled'] = app.enabled

    if app.state == 'absent':
        (installed, out, err) = app.remove()
    else:
        (installed, out, err) = app.install()

        if app.enabled:
            (enabled, out, err) = app.enable()
        else:
            (enabled, out, err) = app.disable()

    result['changed'] = installed or enabled

    if out:
        result['stdout'] = out
    if err:
        result['stderr'] = err

    module.exit_json(**result)

if __name__ == '__main__':
    main()
