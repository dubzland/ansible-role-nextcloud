# Dubzland: Nextcloud
[![Gitlab pipeline status (self-hosted)](https://img.shields.io/gitlab/pipeline/dubzland/ansible-role-nextcloud/main?gitlab_url=https%3A%2F%2Fgit.dubzland.net)](https://git.dubzland.net/dubzland/ansible-role-nextcloud/pipelines)
[![Ansible role downloads](https://img.shields.io/ansible/role/d/49600)](https://galaxy.ansible.com/dubzland/nextcloud)
[![Ansible Quality Score](https://img.shields.io/ansible/quality/49600)](https://galaxy.ansible.com/dubzland/nextcloud)

Installs and configures the Nextcloud personal cloud.

## Requirements

Ansible version 2.0 or higher.

## Role Variables

Available variables are listed below, along with their default values (see
    `defaults/main.yml` for more info):

### dubzland_nextcloud_version

```yaml
dubzland_nextcloud_version: 19.0.0
```

Version of Nextcloud to install

### dubzland_nextcloud_root

```yaml
dubzland_nextcloud_root: "/var/www/nextcloud"
```

Root directory to contain the Nextcloud install.

### dubzland_nextcloud_data_dir

```yaml
dubzland_nextcloud_data_dir: "/srv/nextcloud/data"
```

Directory where Nextcloud will store user data.

### dubzland_nextcloud_db_type

```yaml
dubzland_nextcloud_db_type: sqlite3
```

### dubzland_nextcloud_db_host

```yaml
dubzland_nextcloud_db_host: localhost
```

Host running the database Nextcloud will use.  Only applicable for `pgsql` and
`mysql` db_type.

Type of database.  Allowed options are `sqlite3`, `pgsql` and `mysql`.

### dubzland_nextcloud_db_name

```yaml
dubzland_nextcloud_db_name: nextcloud
```

Name of the Nextcloud database.  The installation process will create this database if it does not exist.

### dubzland_nextcloud_db_username / dubzland_nextcloud_db_password

```yaml
dubzland_nextcloud_db_username: nextcloud
dubzland_nextcloud_db_password: nextcloud
```

Credentials used to connect to the database.  This user will need the `CREATEDB` role.

### dubzland_nextcloud_admin_username / dubzland_nextcloud_admin_password

```yaml
dubzland_nextcloud_admin_username: admin
dubzland_nextcloud_admin_password: nextcloud
```

Credentials to configure for the Nextcloud administrative user.

### dubzland_nextcloud_web_user / dubzland_nextcloud_web_group

```yaml
dubzland_nextcloud_web_user: www-data
dubzland_nextcloud_web_group: www-data
```

System user who should own all Nextcloud application and data files.

### dubzland_nextcloud_url

```yaml
dubzland_nextcloud_url: https://nextcloud.example.com
```

URL where to Nextcloud instance will be accessible.


### dubzland_nextcloud_settings

```yaml
dubzland_nextcloud_settings: []
```

Any additional settings to configure (mail server, etc).  This will be an array
of `key`: `value` dicts.

## Dependencies

None.

## Example Playbook

```yaml
- hosts: nextcloud
  become: yes
  roles:
    - role: dubzland-nextcloud
```

## License

MIT

## Author

* [Josh Williams](https://codingprime.com)
