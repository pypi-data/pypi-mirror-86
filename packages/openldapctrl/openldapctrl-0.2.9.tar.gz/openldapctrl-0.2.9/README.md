# openldapctrl

Simple command tool to setup openldap server.

## Install

```
pip install openldapctrl
```

## Installed Commands

- openldapctrl

## Usage

```
C:\gitlab.zc.local\openldapctrl>openldapctrl --help
Usage: openldapctrl [OPTIONS] COMMAND [ARGS]...

Options:
  --help  Show this message and exit.

Commands:
  add-namespace-entries     Add namespace entries, e.g.
  change-admin-password     Change admin's password.
  init-database             Setup a simple database.
  install-default-schemas   Install default schemas.
  install-schema-idsObject  Add id1, id2, ..., id10 attribute names to user...
  install-server            Yum install openldap servers and related...
  simple-setup              Setup a simple openldap server.
```

## Releases

### v0.2.9 2020/11/21

- Set users base dn to users.accounts.
- Change the permission settings.

### v0.1.18 2020/11/15

- First release.
