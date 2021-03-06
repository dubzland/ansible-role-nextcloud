# Dubzland: Nextcloud
[![Gitlab pipeline status (self-hosted)](https://img.shields.io/gitlab/pipeline/dubzland/ansible-role-nextcloud/main?gitlab_url=https%3A%2F%2Fgit.dubzland.net)](https://git.dubzland.net/dubzland/ansible-role-nextcloud/pipelines)
[![Ansible role](https://img.shields.io/ansible/role/49600)](https://galaxy.ansible.com/dubzland/gitlab)
[![Ansible role downloads](https://img.shields.io/ansible/role/d/49600)](https://galaxy.ansible.com/dubzland/nextcloud)
[![Ansible Quality Score](https://img.shields.io/ansible/quality/49600)](https://galaxy.ansible.com/dubzland/nextcloud)
[![Liberapay patrons](https://img.shields.io/liberapay/patrons/jdubz)](https://liberapay.com/jdubz/donate)
[![Liberapay receiving](https://img.shields.io/liberapay/receives/jdubz)](https://liberapay.com/jdubz/donate)

Installs and configures the Nextcloud personal cloud.

## Requirements

None

## Role Variables

Available variables are listed below, along with their default values (see
    `defaults/main.yml` for more info):

### dubzland_nextcloud_version

```yaml
dubzland_nextcloud_version: "{{ _dubzland_nextcloud_version }}"
```

Version of Nextcloud to install.  Defaults to the most recent version of
Nextcloud compatible with the version of PHP available in the platform's package
manager.

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

Type of database.  Allowed options are `sqlite3`, `pgsql` and `mysql`.

### dubzland_nextcloud_db_host

```yaml
dubzland_nextcloud_db_host: localhost
```

Host running the database Nextcloud will use.  Only applicable for `pgsql` and
`mysql` db_type.

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

### dubzland_nextcloud_cron_frequency

```yaml
dubzland_nextcloud_cron_frequency: '5'
```

How many minutes should elapse between running the cron maintenance job.

### dubzland_nextcloud_url

```yaml
dubzland_nextcloud_url: https://nextcloud.example.com
```

URL where to Nextcloud instance will be accessible.

### dubzland_nextcloud_trusted_domains

```yaml
dubzland_nextcloud_trusted_domains:
  - localhost
  - nextcloud.example.com
```

List of domains allowed to connect to this Nextcloud instance.


### dubzland_nextcloud_settings

```yaml
dubzland_nextcloud_settings: []
```

Any additional settings to configure (mail server, etc).  See
[defaults/main.yml](defaults/main.yml) for examples.

### dubzland_nextcloud_apps

```yaml
dubzland_nextcloud_apps: []
```

Any apps (and their settings) to automatically configure in Nextcloud.  See
[defaults/main.yml](defaults/main.yml) for examples.

## Dependencies

None.

## Example Playbook

```yaml
- hosts: nextcloud
  become: yes
  roles:
    - role: dubzland.nextcloud
```

## License

MIT

## Author

* [Josh Williams](https://dubzland.net)
