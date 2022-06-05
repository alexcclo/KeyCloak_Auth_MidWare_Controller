from keycloak import KeycloakOpenID
import requests

auth_base_url = 'https://authkeycloaktest.azurewebsites.net/auth/'

def set_openid(clientId, clientKey):
        keycloak_openid = KeycloakOpenID(server_url=auth_base_url,
                            realm_name="vastest",
                            client_id=clientId,
                            client_secret_key=clientKey)
        return keycloak_openid

class clientAuth:
    # Get WellKnow
    def getconfig(clientId, clientKey):
        open_id = set_openid(clientId, clientKey)
        return open_id.well_known()
    # Get Token
    def gettoken(clientId, clientKey,username,password):
        open_id = set_openid(clientId, clientKey)
        token = open_id.token(username, password)
        return token
    def get_userinfo(accesstoken):
        user_info_url = auth_base_url+'realms/vastest/protocol/openid-connect/userinfo'
        header = {"Authorization":"Bearer "+accesstoken}
        r = requests.get(user_info_url,headers=header)
        return r.json()
    def refreshtoken(clientId, clientKey,refreshtoken):
        open_id = set_openid(clientId, clientKey)
        token = open_id.refresh_token(refreshtoken)
        return token
