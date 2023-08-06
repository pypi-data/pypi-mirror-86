from guillotina.auth.users import GuillotinaUser
from guillotina.component import get_utility
from guillotina_ldap.interfaces import ILDAPUsers


class LDAPGuillotinaUser(GuillotinaUser):

    async def set_password(self, password):
        util = get_utility(ILDAPUsers)
        await util.set_password(self.id, password)