
import click

from . import services


@click.group()
def main():
    pass

@main.command(name="simple-setup")
@click.option("-d", "--domain", required=True, help="Domain likes like example.com, and it's base dn is dc=example,dc=com.")
@click.option("-a", "--admin", default="admin", help="Admin user's cn name, default to `admin`." )
@click.option("-p", "--admin-password", required=True)
@click.option("-t", "--test", is_flag=True, help="Show ldif content without import.")
@click.option("--hdb-index", type=int, default=2, help="dn=\"olcDatabase={2}hdb,cn=config\" index mostly is 2, but you have change it to fit with your server.")
@click.option("--monitor-index", type=int, default=1, help="dn=\"olcDatabase={2}monitor,cn=config\" index mostly is 1, but you have change it to fit with your server.")
@click.option("--frontend-index", type=int, default=-1, help="dn=\"olcDatabase={2}frontend,cn=config\" index mostly is -1, but you have change it to fit with your server.")
@click.option("-users", "--users-base-path", default="users.accounts", help="Base dn of users. Default to [users.accounts] means cn=users,cn=accounts,dc=example,dc=com")
@click.option("-apps", "--applications-path", default="applications", help="Dn of applications group. Default to [applications] means cn=applications,dc=example,dc=com")
def simple_setup(domain, admin, admin_password, test, hdb_index, monitor_index, frontend_index, users_base_path, applications_path):
    """Setup a simple openldap server.
    """
    services.install_server(test)
    services.install_default_schemas(test)
    services.install_schema_idsObject(test)
    services.init_database(domain, admin, admin_password, test, hdb_index, monitor_index, frontend_index, users_base_path, applications_path)

@main.command(name="install-server")
@click.option("-t", "--test", is_flag=True, help="Show ldif content without import.")
def install_server(test):
    """Yum install openldap servers and related packages.
    """
    return services.install_server(test)

@main.command(name="install-default-schemas")
@click.option("-t", "--test", is_flag=True, help="Show ldif content without import.")
def install_server(test):
    """Install default schemas.
    """
    return services.install_default_schemas(test)

@main.command(name="install-schema-idsObject")
@click.option("-t", "--test", is_flag=True, help="Show ldif content without import.")
def install_schema_idsObject(test):
    """Add id1, id2, ..., id10 attribute names to user entry.
    """
    return services.install_schema_idsObject(test)

@main.command(name="init-database")
@click.option("-d", "--domain", required=True, help="Domain likes like example.com, and it's base dn is dc=example,dc=com.")
@click.option("-a", "--admin", default="admin", help="Admin user's cn name, default to `admin`." )
@click.option("-p", "--admin-password", required=True)
@click.option("-t", "--test", is_flag=True, help="Show ldif content without import.")
@click.option("--hdb-index", type=int, default=2, help="dn=\"olcDatabase={2}hdb,cn=config\" index mostly is 2, but you have change it to fit with your server.")
@click.option("--monitor-index", type=int, default=1, help="dn=\"olcDatabase={2}monitor,cn=config\" index mostly is 1, but you have change it to fit with your server.")
@click.option("--frontend-index", type=int, default=-1, help="dn=\"olcDatabase={2}frontend,cn=config\" index mostly is -1, but you have change it to fit with your server.")
@click.option("-users", "--users-base-path", default="users.accounts", help="Base dn of users. Default to [users.accounts] means cn=users,cn=accounts,dc=example,dc=com")
@click.option("-apps", "--applications-path", default="applications", help="Dn of applications group. Default to [applications] means cn=applications,dc=example,dc=com")
def init_database(domain, admin, admin_password, test, hdb_index, monitor_index, frontend_index, users_base_path, applications_path):
    """Setup a simple database.
    """
    return services.init_database(domain, admin, admin_password, test, hdb_index, monitor_index, frontend_index, users_base_path, applications_path)

@main.command(name="add-namespace-entries")
@click.option("-t", "--test", is_flag=True, help="Show ldif content without import.")
@click.option("-d", "--domain")
@click.argument("path", nargs=1, required=True)
def add_namespace_entries(path, domain, test):
    """Add namespace entries, e.g. cn=users,dc=example,dc=com.
    """
    return services.add_namespace_entries(path, domain, test)

@main.command(name="change-admin-password")
@click.option("-p", "--password", required=True)
@click.option("-t", "--test", is_flag=True, help="Show ldif content without import.")
@click.option("--hdb-index", type=int, default=2, help="dn=\"olcDatabase={2}hdb,cn=config\" index mostly is 2, but you have change it to fit with your server.")
def change_admin_password(password, hdb_index, test):
    """Change admin's password.
    """
    return services.change_admin_password(password, hdb_index, test)

@main.command(name="uninstall")
@click.option("-t", "--test", is_flag=True, help="Show ldif content without import.")
def uninstall(test):
    """Uninstall openldap and clean all data.
    """
    return services.uninstall(test)

if __name__ == "__main__":
    main()
