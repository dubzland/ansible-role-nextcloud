#!/usr/bin/python

# Copyright: (c) 2019, Josh Williams <vmizzle@gmail.com>
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function
__metaclass__ = type

ANSIBLE_METADATA = {'metadata_version': '1.1',
                    'status': ['preview'],
                    'supported_by': 'community'}

DOCUMENTATION = '''
---
module: nextcloud_config

short_description: Configures Nextcloud (via occ config:set)

version_added: "2.2"

description:
    - "Sets Nextcloud configuration options (via occ config:set)"

options:
    name:
        required: true
        description:
            - Name of the setting
    type:
        required: true
        choices: ["system", "app"]
        description:
            - Type of setting (app or system)
    value:
        description:
            - Value to be set
        required: true
    state:
        choices: ["present", "absent"]
        default: "present"
        description:
            - Desired setting state
    index:
        default: None
        description:
            - For options that require an index (such as trusted_domains)
    nextcloud_root:
        required: true
        description:
            - Nextcloud root directory
'''

from ansible.module_utils.basic import AnsibleModule

class NextcloudSetting(object):
    def __init__(self, module):
        self.module         = module
        self.state          = module.params['state']
        self.type           = module.params['type']
        self.name           = module.params['name']
        self.value          = module.params['value']
        self.index          = module.params['index']
        self.nextcloud_root = module.params['nextcloud_root']

    def exec_cmd(self, cmd):
        return self.module.run_command(cmd, cwd=self.nextcloud_root)

    def get_value(self):
        if self.index != None:
            thecmd = "php occ config:%s:get --default-value='' %s %d" % (self.type, self.name, self.index)
        else:
            thecmd = "php occ config:%s:get %s" % (self.type, self.name)

        # (rc, out, err) = self.exec_cmd(thecmd)
        # return (rc, out, err, thecmd)
        return self.exec_cmd(thecmd)


    def set_value(self):
        if self.index != None:
            thecmd = 'php occ config:%s:set %s %d --value="%s"' % (self.type, self.name, self.index, self.value)
        else:
            thecmd = 'php occ config:%s:set %s --value="%s"' % (self.type, self.name, self.value)

        # (rc, out, err) = self.exec_cmd(thecmd)
        # return (rc, out, err, thecmd)
        return self.exec_cmd(thecmd)


def main():
    module = AnsibleModule(
        argument_spec=dict(
            name=dict(type='str', required=True),
            state=dict(type='str', default='present', choices=['absent', 'present']),
            type=dict(type='str', default='system', choices=['system', 'app']),
            value=dict(type='str', required=True),
            index=dict(type='int', default=None),
            nextcloud_root=dict(type='str', required=True),
        ),
        supports_check_mode=True,
    )

    setting = NextcloudSetting(module)
    rc = 0
    out = ''
    err = ''
    cmd = ''
    result = {}
    result['name'] = setting.name
    result['state'] = setting.state

    # (rc, out, err, cmd) = setting.get_value()
    (rc, out, err) = setting.get_value()
    if rc != 0:
        msg = "rc: %s, err: [%s], out: [%s], cmd: [%s], Fail #1" % (rc, err, out, cmd)
        module.fail_json(name=setting.name, msg=err)

    current = out.strip()

    if setting.state == 'absent':
        if len(current) == 0:
            if module.check_mode:
                module.exit_json(changed=False)
        else:
            if module.check_mode:
                module.exit_json(changed=True)
            else:
                # (rc, out, err, cmd) = setting.set_value()
                (rc, out, err) = setting.set_value()
                if rc != 0:
                    module.fail_json(name=setting.name, msg=err)
    else:
        if current == setting.value:
            rc = None
        else:
            if module.check_mode:
                module.exit_json(changed=True)

            # (rc, out, err, cmd) = setting.set_value()
            (rc, out, err) = setting.set_value()
            if rc != 0:
                module.fail_json(name=setting.name, msg=err)

    if rc is not None and rc != 0:
        module.fail_json(name=setting.name, msg=err)

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
