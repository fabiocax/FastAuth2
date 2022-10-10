from ldap3 import Server, Connection, ALL, SUBTREE
from ldap3.core.exceptions import LDAPException, LDAPBindError, LDAPSocketOpenError
from ldap3.utils.conv import escape_filter_chars
from os import environ


ldap_server_uri=environ["ldap_server_uri"]
ldap_base=environ["ldap_base"]
ldap_filter=environ["ldap_filter"]
ldap_user_admin=environ["ldap_user_admin"]
ldap_user_password=environ["ldap_user_password"]

class ldap_test():
    def __init__(self):
        self.ldap_server = Server(ldap_server_uri, get_info=ALL)
        self.ldap_connection = Connection(self.ldap_server, user =ldap_user_admin ,password=ldap_user_password, auto_bind=True)

    def ldap(self,uid,password):
        try:     

            if self.ldap_connection.bind() == True:
                if self.ldap_connection.search(search_base=ldap_base, search_filter=ldap_filter,search_scope = SUBTREE) == True:
                    uid=((str(self.ldap_connection.entries).split(' ')[1]))
                    
                    try:
                        ldap_user_connection = Connection(self.ldap_server, user = uid, password=password, auto_bind=True)
                        
                        if ldap_user_connection.bind() == True:
                            entry=True
                        else:
                            entry=False
                    except LDAPBindError:
                        entry=False

                    
                    return entry
                else:
                    return None
        except LDAPSocketOpenError:
            print('Unabled to connect to the LDAP server!')
            return None


#print(ldap_test().ldap('fabio','n0r0nh4'))
