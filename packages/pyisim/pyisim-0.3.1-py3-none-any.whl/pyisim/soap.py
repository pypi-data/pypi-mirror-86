from zeep import Client, Settings
from zeep.xsd import Nil
from zeep.transports import Transport
from zeep.helpers import serialize_object
from zeep.cache import InMemoryCache

# from isim_classes import StaticRole
import requests
from pyisim.exceptions import NotFoundError

# from pyisim.entities import OrganizationalContainer


requests.packages.urllib3.disable_warnings()  # type: ignore


class ISIMClient:
    def __init__(self, url, user_, pass_, cert_path=None):

        self.addr = url + "/itim/services/"
        self.cert_path = cert_path
        self.s = self.login(user_, pass_)

    def login(self, user_, pass_):
        url = self.addr + "WSSessionService?wsdl"
        assert self.cert_path is not None, "No certificate passed"
        client = self.get_client(url)
        session = client.service.login(user_, pass_)
        return session

    def get_client(self, url):

        # Si ya se inicializó el cliente especificado en client_name, lo devuelve. Si no, lo inicializa, setea y devuelve.
        # ej. -> https://<ITIMURL>/.../WSSessionService?wsdl -> wssessionservice
        client_name = url.split("/")[-1][:-5].lower()
        client = getattr(self, client_name, None)

        if client is None:
            settings = Settings(strict=False)
            s = requests.Session()
            s.verify = self.cert_path
            client = Client(
                url,
                settings=settings,
                transport=Transport(session=s, cache=InMemoryCache()),
            )
            # necesario porque los WSDL de SIM queman el puerto y no funciona con balanceador
            client.service._binding_options["address"] = url[:-5]
            setattr(self, client_name, client)

        return client

    def lookup_container(self, dn):

        url = self.addr + "WSOrganizationalContainerServiceService?wsdl"
        client = self.get_client(url)

        cont = client.service.lookupContainer(self.s, dn)

        return cont

    def search_organization(self, perfil, nombre):

        url = self.addr + "WSOrganizationalContainerServiceService?wsdl"
        client = self.get_client(url)

        ous = client.service.searchContainerByName(self.s, Nil, perfil, nombre)

        return ous

    def search_provisioning_policy(self, wsou, nombre_politica, find_unique=True):

        url = self.addr + "WSProvisioningPolicyServiceService?wsdl"
        client = self.get_client(url)

        politicas = client.service.getPolicies(self.s, wsou, nombre_politica)

        if find_unique:
            assert (
                len(politicas) > 0
            ), f"No se ha encontrado la política {nombre_politica}."
            assert (
                len(politicas) == 1
            ), f"Se ha encontrado más de la política con: {nombre_politica}"
            return politicas[0]
        else:
            return politicas

    def add_provisioning_policy(self, ou, wsprovisioningpolicy, date):

        url = self.addr + "WSProvisioningPolicyServiceService?wsdl"
        client = self.get_client(url)

        s = client.service.createPolicy(self.s, ou, wsprovisioningpolicy, date)

        return s

    def modify_provisioning_policy(self, ou, wsprovisioningpolicy, date):

        url = self.addr + "WSProvisioningPolicyServiceService?wsdl"
        client = self.get_client(url)

        s = client.service.modifyPolicy(self.s, ou, wsprovisioningpolicy, date)

        return s

    def delete_provisioning_policy(self, ou, dn, date):
        url = self.addr + "WSProvisioningPolicyServiceService?wsdl"
        client = self.get_client(url)

        s = client.service.deletePolicy(self.s, ou, dn, date)

        return s

    def search_role(self, filtro, find_unique=True):

        url = self.addr + "WSRoleServiceService?wsdl"
        client = self.get_client(url)

        roles = client.service.searchRoles(self.s, filtro)

        if find_unique:
            assert (
                len(roles) > 0
            ), f"No se ha encontrado el rol con el filtro: {filtro}. Verifique que sea un filtro LDAP válido."
            assert len(roles) == 1, f"Se ha encontrado más de un rol con: {filtro}"
            return roles[0]
        else:
            return roles

    def lookup_role(self, dn):

        url = self.addr + "WSRoleServiceService?wsdl"
        client = self.get_client(url)

        try:
            r = client.service.lookupRole(self.s, dn)
            return r
        except:
            raise NotFoundError("Rol no encontrado")

    def create_static_role(self, wsrole, wsou):

        url = self.addr + "WSRoleServiceService?wsdl"
        client = self.get_client(url)

        return client.service.createStaticRole(self.s, wsou, wsrole)

    def modify_static_role(self, role_dn, wsattr_list):

        url = self.addr + "WSRoleServiceService?wsdl"
        client = self.get_client(url)

        return client.service.modifyStaticRole(self.s, role_dn, wsattr_list)

    def remove_role(self, role_dn, date=None):

        url = self.addr + "WSRoleServiceService?wsdl"
        client = self.get_client(url)

        if date:
            raise NotImplementedError()
        else:
            date = Nil
        return client.service.removeRole(self.s, role_dn, date)

    def search_people(self, filtro):

        url = self.addr + "WSPersonServiceService?wsdl"
        client = self.get_client(url)

        personas = client.service.searchPersonsFromRoot(self.s, filtro, Nil)

        assert (
            len(personas) > 0
        ), f"No se ha encontrado la persona con el filtro: {filtro}. Verifique que sea un filtro LDAP válido."
        assert len(personas) == 1, f"Se ha encontrado más de una persona con: {filtro}"
        return personas[0]

    def search_service(self, ou, filtro, find_unique=True):

        url = self.addr + "WSServiceServiceService?wsdl"
        client = self.get_client(url)
        servicios = client.service.searchServices(self.s, ou, filtro)

        if find_unique:
            if len(servicios) == 0:
                raise NotFoundError(
                    f"No se ha encontrado el servicio con el filtro:  {filtro}. Verifique que sea un filtro LDAP válido."
                )
            assert (
                len(servicios) == 1
            ), f"Se ha encontrado más de un servicio con: {filtro}"
            return servicios[0]
        else:
            return servicios

    def search_workflow(self, nombre, org_name):
        """
        Busca flujos de cuenta y acceso por el nombre.
        Retorna el DN.
        """

        url = self.addr + "WSSearchDataServiceService?wsdl"
        client = self.get_client(url)

        """
        Category puede ser (usar EstaCapitalizacion y quitar _):
        ACCESS_TYPE, ACCOUNT_TEMPLATE, ADOPTION_POLICY, AGENT_OPERATION, ATTRIBUTE_CONSTRAINT, 
        BPUNIT, CATEGORIES_FOR_LIFE_CYCLE_MGT, CONFIG, CONTAINER, CREDENTIAL, CREDENTIAL_COMPONENT, 
        CREDENTIAL_LEASE, CREDENTIAL_POOL, CREDENTIAL_SERVICE, CUSTOM_PROCESS, DYNAMIC_ROLE, FORM_TEMPLATE, 
        GLOBAL_ACCOUNT_TEMPLATE, GROUP, HOST_SELECTION_POLICY, IDENTITY_POLICY, JOIN_DIRECTIVE, JOINDIRECTIVE, 
        LIFECYCLE_PROFILE, LOCATION, OBJECT_PROFILE, ORG, ORGROLE, ORGUNIT, ORPHANED_ACCOUNT, OWNERSHIP_TYPE, 
        PASSWORD_POLICY, PRIVILEGE_RULE, PROVISIONING_POLICY, RECERTIFICATION_POLICY, ROLE, SECURITY_DOMAIN, 
        SEPARATION_OF_DUTY_POLICY, SEPARATION_OF_DUTY_RULE, SERVICE, SERVICE_MODEL, SERVICE_PROFILE, 
        SHARED_ACCESS_POLICY, SYSTEM_ROLE, SYSTEM_USER, TENANT, USERACCESS
        """
        flujos = client.service.findSearchControlObjects(
            self.s,
            {
                "objectclass": "erWorkflowDefinition",
                "contextDN": f"ou=workflow,erglobalid=00000000000000000000,ou={org_name},dc={org_name}",
                "returnedAttributeName": "dn",
                "filter": f"(erProcessName={nombre})",
                "base": "global",
                "category": "CustomProcess",
            },
        )

        assert (
            len(flujos) > 0
        ), f"No se ha encontrado el flujo: {nombre}. Verifique que sea un filtro LDAP válido."
        assert len(flujos) == 1, f"Se ha encontrado más de un servicio con: {nombre}"

        return flujos[0]["value"]

    def get_groups_by_service(self, dn_servicio, profile_name, info):

        url = self.addr + "WSGroupServiceService?wsdl"
        client = self.get_client(url)

        grps = client.service.getGroupsByService(
            self.s, dn_servicio, profile_name, info
        )
        return grps

    def get_activities_recursive(self, process_id, act_list):
        url = self.addr + "WSRequestServiceService?wsdl"
        client = self.get_client(url)

        acts = client.service.getActivities(self.s, int(process_id), False)
        act_list.extend(acts)

        subprocesses = client.service.getChildProcesses(self.s, int(process_id))
        for s in subprocesses:
            self.get_activities_recursive(s.requestId, act_list)
        return "ok"

    def get_request_activities(self, process_id, pending_only=True):
        """
        The customer can accomplish this by using a combination of getActivities() and getChildProcesses().
        """
        # url = self.addr + "WSRequestServiceService?wsdl"
        # client = self.get_client(url)

        actividades = []
        self.get_activities_recursive(int(process_id), actividades)

        # Filtra solo las actividades manuales (M) y pendientes (R)
        if pending_only:
            actividades = [
                a for a in actividades if a.activityType == "M" and a.state == "R"
            ]

        return actividades

    def suspend_person(self, dn, justification):
        # suspendPerson(session: ns1:WSSession, personDN: xsd:string, justification: xsd:string)
        url = self.addr + "WSPersonServiceService?wsdl"
        client = self.get_client(url)

        r = client.service.suspendPerson(self.s, dn, justification)
        return r

    def restore_person(self, dn, restore_accounts, password, date, justification):
        # restorePerson(session: ns1:WSSession, personDN: xsd:string, restoreAccounts: xsd:boolean, password: xsd:string, date: xsd:dateTime, justification: xsd:string) -> restorePersonReturn: ns1:WSRequest
        url = self.addr + "WSPersonServiceService?wsdl"
        client = self.get_client(url)

        if date:
            raise NotImplementedError()
        else:
            date = Nil

        r = client.service.restorePerson(
            self.s, dn, restore_accounts, password or Nil, date, justification
        )
        return r

    def delete_person(self, dn, justification):
        # deletePerson(session: ns1:WSSession, personDN: xsd:string, date: xsd:dateTime, justification: xsd:string) -> deletePersonReturn: ns1:WSRequest
        url = self.addr + "WSPersonServiceService?wsdl"
        client = self.get_client(url)

        r = client.service.deletePerson(self.s, dn, Nil, justification)
        return r

    def create_dynamic_role(self, wsrole, wsou, date=None):

        url = self.addr + "WSRoleServiceService?wsdl"
        client = self.get_client(url)

        if date:
            raise NotImplementedError()
        else:
            date = Nil

        return client.service.createDynamicRole(self.s, wsou, wsrole, date)

    def modify_dynamic_role(self, role_dn, wsattr_list, date=None):

        url = self.addr + "WSRoleServiceService?wsdl"
        client = self.get_client(url)

        if date:
            raise NotImplementedError()
        else:
            date = Nil

        return client.service.modifyDynamicRole(self.s, role_dn, wsattr_list, date)

    def get_default_account_attributes_by_person(self, service_dn, person_dn):
        url = self.addr + "WSAccountServiceService?wsdl"
        client = self.get_client(url)

        r = client.service.getDefaultAccountAttributesByPerson(
            self.s, service_dn, person_dn
        )
        return r

    def get_default_account_attributes(self, service_dn):
        url = self.addr + "WSAccountServiceService?wsdl"
        client = self.get_client(url)

        r = client.service.getDefaultAccountAttributes(self.s, service_dn)
        return r

    def get_account_profile_for_service(self, service_dn):
        url = self.addr + "WSAccountServiceService?wsdl"
        client = self.get_client(url)

        r = client.service.getAccountProfileForService(self.s, service_dn)
        return r

    def search_accounts(self, search_arguments):
        url = self.addr + "WSAccountServiceService?wsdl"
        client = self.get_client(url)

        search_arguments = {k: v for k, v in search_arguments.items() if v is not None}

        r = client.service.searchAccounts(self.s, search_arguments)
        return r

    # createAccount(session: ns1:WSSession, serviceDN: xsd:string, wsAttrs: ns1:WSAttribute[], date: xsd:dateTime, justification: xsd:string) -> createAccountReturn: ns1:WSRequest
    def create_account(self, service_dn, wsattrs, date, justification):
        url = self.addr + "WSAccountServiceService?wsdl"
        client = self.get_client(url)

        if date:
            raise NotImplementedError()
        else:
            date = Nil

        r = client.service.createAccount(
            self.s, service_dn, wsattrs, date, justification
        )
        return r

    # getAccountsByOwner(session: ns1:WSSession, personDN: xsd:string) -> getAccountsByOwnerReturn: ns1:WSAccount[]
    def get_accounts_by_owner(self, person_dn):
        url = self.addr + "WSPersonServiceService?wsdl"
        client = self.get_client(url)

        r = client.service.getAccountsByOwner(self.s, person_dn)
        return r

    # suspendAccount(session: ns1:WSSession, accountDN: xsd:string, date: xsd:dateTime, justification: xsd:string) -> suspendAccountReturn: ns1:WSRequest
    def suspend_account(self, account_dn, date, justification):
        url = self.addr + "WSAccountServiceService?wsdl"
        client = self.get_client(url)

        if date:
            raise NotImplementedError()
        else:
            date = Nil

        r = client.service.suspendAccount(self.s, account_dn, date, justification)
        return r

    # restoreAccount(session: ns1:WSSession, accountDN: xsd:string, newPassword: xsd:string, date: xsd:dateTime, justification: xsd:string) -> restoreAccountReturn: ns1:WSRequest
    def restore_account(self, account_dn, password, date, justification):
        url = self.addr + "WSAccountServiceService?wsdl"
        client = self.get_client(url)

        if date:
            raise NotImplementedError()
        else:
            date = Nil

        r = client.service.restoreAccount(
            self.s, account_dn, password, date, justification
        )
        return r

    # deprovisionAccount(session: ns1:WSSession, accountDN: xsd:string, date: xsd:dateTime, justification: xsd:string) -> deprovisionAccountReturn: ns1:WSRequest
    def deprovision_account(self, account_dn, date, justification):
        url = self.addr + "WSAccountServiceService?wsdl"
        client = self.get_client(url)

        if date:
            raise NotImplementedError()
        else:
            date = Nil

        r = client.service.deprovisionAccount(self.s, account_dn, date, justification)
        return r

    # orphanSingleAccount(session: ns1:WSSession, accountDN: xsd:string) ->
    def orphan_single_account(self, account_dn):
        url = self.addr + "WSAccountServiceService?wsdl"
        client = self.get_client(url)

        r = client.service.orphanSingleAccount(self.s, account_dn)
        return r

    # modifyAccount(session: ns1:WSSession, accountDN: xsd:string, wsAttrs: ns1:WSAttribute[], date: xsd:dateTime, justification: xsd:string) -> modifyAccountReturn: ns1:WSRequest
    def modify_account(self, account_dn, wsattrs, date, justification):
        url = self.addr + "WSAccountServiceService?wsdl"
        client = self.get_client(url)

        if date:
            raise NotImplementedError()
        else:
            date = Nil

        r = client.service.modifyAccount(
            self.s, account_dn, wsattrs, date, justification
        )
        return r

    def suspend_person_advanced(self, person_dn, include_accounts, date, justification):
        # suspendPersonAdvanced(session: ns1:WSSession, personDN: xsd:string, includeAccounts: xsd:boolean, date: xsd:dateTime, justification: xsd:string) -> suspendPersonAdvancedReturn: ns1:WSRequest
        url = self.addr + "WSPersonServiceService?wsdl"
        client = self.get_client(url)

        if date:
            raise NotImplementedError()
        else:
            date = Nil

        r = client.service.suspendPersonAdvanced(
            self.s, person_dn, include_accounts, date, justification
        )
        return r

    def get_request(self, request_id):
        # getRequest(session: ns1:WSSession, requestId: xsd:long) -> getRequestReturn: ns1:WSRequest
        url = self.addr + "WSRequestServiceService?wsdl"
        client = self.get_client(url)
        r = client.service.getRequest(self.s, request_id)
        return r

    def abort_request(self, request_id, justification):
        # abortRequest(session: ns1:WSSession, requestId: xsd:long, justification: xsd:string) ->
        url = self.addr + "WSRequestServiceService?wsdl"
        client = self.get_client(url)
        r = client.service.abortRequest(self.s, request_id, justification)
        return r
