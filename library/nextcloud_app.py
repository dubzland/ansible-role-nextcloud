#!/usr/bin/python

# Copyright: (c) 2019, Josh Williams <vmizzle@gmail.com>
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function
import json
__metaclass__ = type

ANSIBLE_METADATA = {'metadata_version': '1.1',
                    'status': ['preview'],
                    'supported_by': 'community'}

DOCUMENTATION = '''
---
module: nextcloud_app

short_description: Adds (or removes) Nextcloud apps.

description:
    - "Adds or removes apps from Nextcloud.

options:
    name:
        required: true
        description:
            - Name of the app
    state:
        choices: ["present", "absent"]
        default: "present"
        description:
            - Whether the app should be present or absent.
    enabled:
        choices: ["yes", "no"]
        default: "yes"
        description:
            - Whether or not the app should be enabled within Nextcloud
    nextcloud_root:
        required: true
        description:
            - Nextcloud root directory
'''

from ansible.module_utils.basic import AnsibleModule

class NextcloudApp(object):
    def __init__(self, module):
        self.module         = module
        self.name           = module.params['name']
        self.state          = module.params['state']
        self.enabled        = module.params['enabled']
        self.nextcloud_root = module.params['nextcloud_root']

    def exec_cmd(self, cmd):
        return self.module.run_command(cmd, cwd=self.nextcloud_root)

    def get_app_list(self):
        (rc, out, err) = self.exec_cmd("php occ app:list --output=json")
        if rc != 0:
            return self.module.fail_json(name=self.name, msg=err)

        self.apps = json.loads(out)

        return (rc, out, err)

    def is_installed(self):
        return ((self.name in self.apps['enabled']) or (self.name in
            self.apps['disabled']))

    def is_enabled(self):
        if self.is_installed:
            return self.name in self.apps['enabled']
        else:
            return False

    def install(self):
        thecmd = "php occ app:install %s" % self.name
        return self.exec_cmd(thecmd)

    def remove(self):
        thecmd = "php occ app:remove %s" % self.name
        return self.exec_cmd(thecmd)

    def enable(self):
        thecmd = "php occ app:enable %s" % self.name
        return self.exec_cmd(thecmd)

    def disable(self):
        thecmd = "php occ app:disable %s" % self.name
        return self.exec_cmd(thecmd)

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
    rc = 0
    out = ''
    err = ''
    result = {}
    result['name'] = app.name
    result['state'] = app.state

    (rc, out, err) = app.get_app_list()
    if rc != 0:
        msg = "rc: %s, err: [%s], out: [%s]" % (rc, err, out)
        module.fail_json(name=setting.name, msg=err)

    if app.state == 'absent':
        if app.is_installed():
            if module.check_mode:
                module.exit_json(changed=True)
            else:
                (rc, out, err) = app.remove()
                if rc != 0:
                    module.fail_json(name=app.name, msg=err)
        else:
            module.exit_json(changed=False)
    else:
        if app.is_installed():
            if app.enabled:
                if app.is_enabled():
                    rc = None
                else:
                    (rc, out, err) = app.enable()
                    if rc != 0:
                        module.fail_json(name=app.name, msg=err)
            else:
                if app.is_enabled():
                    (rc, out, err) = app.disable()
                    if rc != 0:
                        module.fail_json(name=app.name, msg=err)
                else:
                    rc = None
        else:
            (rc, out, err) = app.install()
            if rc != 0:
                module.fail_json(name=app.name, msg=err)

            if not app.enabled:
                (rc, out, err) = app.disable()
                if rc != 0:
                    module.fail_json(name=app.name, msg=err)

    if rc is not None and rc != 0:
        module.fail_json(name=app.name, msg=err)

    if rc is None:
        result['changed'] = False
    else:
        result['changed'] = True

    if out:
        result['stdout'] = out
    if err:
        result['stderr'] = err

    module.exit_json(**result)

if __name__ == '__main__':
    main()
