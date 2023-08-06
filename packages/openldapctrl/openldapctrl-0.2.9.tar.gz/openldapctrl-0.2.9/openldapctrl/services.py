import os

from fastutils import hashutils
from fastutils import fsutils
import ldaputils

data_root = os.path.abspath(os.path.join(os.path.dirname(__file__), "./data"))


def install_server(test):
    print("#"*40)
    print("# install server")
    print("#"*40)
    cmd = "yum install -y openldap-servers openldap-clients compat-openldap openldap-devel"
    print(cmd)
    if not test:
        os.system(cmd)
    
    cmd = "cp -f /usr/share/openldap-servers/DB_CONFIG.example /var/lib/ldap/DB_CONFIG"
    print(cmd)
    if not test:
        os.system(cmd)

    cmd = "systemctl enable slapd"
    print(cmd)
    if not test:
        os.system(cmd)
    
    cmd = "systemctl start slapd"
    print(cmd)
    if not test:
        os.system(cmd)

def install_default_schemas(test):
    print("#"*40)
    print("# install default schemas")
    print("#"*40)
    default_schemas = [x.strip() for x in """
        /etc/openldap/schema/core.ldif
        /etc/openldap/schema/cosine.ldif
        /etc/openldap/schema/openldap.ldif
        /etc/openldap/schema/inetorgperson.ldif
        /etc/openldap/schema/nis.ldif
        /etc/openldap/schema/collective.ldif
        /etc/openldap/schema/corba.ldif
        /etc/openldap/schema/duaconf.ldif
        /etc/openldap/schema/dyngroup.ldif
        /etc/openldap/schema/java.ldif
        /etc/openldap/schema/misc.ldif
        /etc/openldap/schema/pmi.ldif
        /etc/openldap/schema/ppolicy.ldif
    """.splitlines() if x.strip()]
    for schema in default_schemas:
        print("load schema: {}".format(schema))
        if not test:
            ldaputils.ldapimport(schema)

def install_schema_idsObject(test):
    print("#"*40)
    print("# install idsObject schemas")
    print("#"*40)
    schema_ldif_filepath = os.path.abspath(os.path.join(data_root, "./schema.idsObject.ldif"))
    print("load schema: {}".format(schema_ldif_filepath))
    if not test:
        ldaputils.ldapimport(schema_ldif_filepath)

def add_base_entry(domain, test):
    print("#"*40)
    print("# add base entry")
    print("#"*40)
    base_dn = ldaputils.get_base_dn_from_domain(domain)
    dc = domain.split(".")[0]
    base_template_filepath = os.path.abspath(os.path.join(data_root, "./template.base.ldif"))
    base_template = fsutils.readfile(base_template_filepath)
    base_content = base_template.format(base_dn=base_dn, dc=dc)
    print(base_content)
    with fsutils.TemporaryFile(content=base_content) as fileinstance:
        if not test:
            ldaputils.ldapimport(fileinstance.filepath)

def add_namespace_entries(path, domain, test):
    print("#"*40)
    print("# add namespace {0}".format(path))
    print("#"*40)
    if not path:
        return
    namespace_template_filepath = os.path.abspath(os.path.join(data_root, "./template.namespace.ldif"))
    namespace_template = fsutils.readfile(namespace_template_filepath)

    paths = path.split(".")
    if not domain:
        domains = paths[-2:]
        paths = paths[:-2]
        domain = ".".join(domains)
    else:
        domains = domain.split(".")

    ldif_sections = []
    while len(paths):
        cn = paths[0]
        path = ".".join(paths)
        dn = ldaputils.get_dn_from_path(path, domain)
        section = namespace_template.format(dn=dn, cn=cn)
        ldif_sections.append(section)
        paths = paths[1:]
    ldif_sections.reverse()

    ldif_content = "\n\n".join(ldif_sections)
    print(ldif_content)
    with fsutils.TemporaryFile(content=ldif_content) as fileinstance:
        if not test:
            ldaputils.ldapimport(fileinstance.filepath)

def get_namespace_read_perms(path, admin, domain):
    namespace_read_perm_template_filepath = os.path.abspath(os.path.join(data_root, "./template.namespace.read.perm.ldif"))
    namespace_read_perm_template = fsutils.readfile(namespace_read_perm_template_filepath)
    admin_dn = ldaputils.get_dn_from_path(admin, domain)
    ldif_sections = []
    paths = path.split(".")
    while len(paths):
        path = ".".join(paths)
        dn = ldaputils.get_dn_from_path(path, domain)
        section = namespace_read_perm_template.format(dn=dn, admin_dn=admin_dn)
        ldif_sections.append(section)
        paths = paths[1:]
    ldif_sections.reverse()
    ldif_content = "\n".join(ldif_sections)
    return ldif_content

def add_applications_entry(applications_path, admin, domain, test):
    applications_dn = ldaputils.get_dn_from_path(applications_path, domain)
    admin_dn = ldaputils.get_dn_from_path(admin, domain)
    applications_template_filepath = os.path.abspath(os.path.join(data_root, "./template.applications.ldif"))
    ldaputils.ldap_template_import(applications_template_filepath, {
        "applications_dn": applications_dn,
        "admin_dn": admin_dn,
    }, test=test)

def init_database(domain, admin, admin_password, test, hdb_index, monitor_index, frontend_index, users_base_path, applications_path):
    print("#"*40)
    print("# init database")
    print("#"*40)
    
    base_dn = ldaputils.get_base_dn_from_domain(domain)
    admin_dn = ldaputils.get_dn_from_path(admin, domain)
    users_dn_read_perm = get_namespace_read_perms(users_base_path, admin, domain)
    admin_perm_ldif_template_filepath = os.path.abspath(os.path.join(data_root, "./template.init.ldif"))
    admin_password_encoded = "{SHA}" + hashutils.get_sha1_base64(admin_password)
    ldaputils.ldap_template_import(admin_perm_ldif_template_filepath, dict(
        base_dn=base_dn,
        hdb_index=hdb_index,
        monitor_index=monitor_index,
        frontend_index=frontend_index,
        admin_dn=admin_dn,
        admin_password_encoded=admin_password_encoded,
        users_dn_read_perm=users_dn_read_perm,
        users_base_dn=ldaputils.get_dn_from_path(users_base_path, domain),
        applications_dn=ldaputils.get_dn_from_path(applications_path, domain),
    ), test=test)

    add_base_entry(domain, test)
    add_namespace_entries(admin, domain, test)
    add_namespace_entries(users_base_path, domain, test)
    add_namespace_entries(".".join(applications_path.split(".")[1:]), domain, test)
    add_applications_entry(applications_path, admin, domain, test)
    

def change_admin_password(password, hdb_index, test):
    print("#"*40)
    print("# change admin password")
    print("#"*40)
    ldaputils.ldap_template_import("template.change-admin-password.ldif", {
        "hdb_index": hdb_index,
        "admin_password_encoded": "{SHA}" + hashutils.get_sha1_base64(password),
    }, data_root, test)


def uninstall(test):
    print("#"*40)
    print("# Uninstall openldap and clean it's data.")
    print("#"*40)

    cmd = "yum remove -y openldap-servers openldap-clients compat-openldap openldap-devel"
    print(cmd)
    if not test:
        os.system(cmd)

    cmd = "rm -rf /tmp/openldap-tlsmc-certs*"
    print(cmd)
    if not test:
        os.system(cmd)

    cmd = "rm -rf /var/lib/ldap/*"
    print(cmd)
    if not test:
        os.system(cmd)

    cmd = "rm -rf /etc/openldap/slapd.d/"
    print(cmd)
    if not test:
        os.system(cmd)

    cmd = "rm -rf /etc/openldap/schema/"
    print(cmd)
    if not test:
        os.system(cmd)
