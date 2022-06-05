from flask import Flask,redirect,request
from flask_restplus import Api, Resource, fields
from werkzeug.contrib.fixers import ProxyFix
from authcenter import clientAuth

app = Flask(__name__)
app.wsgi_app = ProxyFix(app.wsgi_app)

api = Api(app, version='1.0', title='WiAdvance Auth Center',
    description='WiAdvance Auth Center Midware',
)
# remove default namespace
api.namespaces.pop(0)

accesstoken_postpraser = api.model('payload', {
    'client_id': fields.String(required=True, description='client_id'),
    'client_secret': fields.String(required=True, description='client_secret'),
    'username': fields.String(required=True, description='username'),
    'password': fields.String(required=True, description='password')
})

token_validate_postpraser = api.model('token', {
    'access_token': fields.String(required=True, description='access_token'),
})

token_refresh_postpraser = api.model('token', {
    'client_id': fields.String(required=True, description='client_id'),
    'client_secret': fields.String(required=True, description='client_secret'),
    'refresh_token': fields.String(required=True, description='refresh_token'),
})
# CLIENT
ns_client = api.namespace('client', description='Client Authorization')


@ns_client.route('/Auth')
class Client(Resource):
    @ns_client.param('client_id', 'client_id')
    @ns_client.param('redirect_url', 'redirect_url')
    @ns_client.param('scope', 'scope')
    def get(self):
        args = request.args
        print(args)
        client_id = args.get('client_id')
        redirect_url = args.get('redirect_url')
        scope = args.get('scope')
        auth_url = 'https://authkeycloaktest.azurewebsites.net/auth/realms/vastest/protocol/openid-connect/auth?client_id='+client_id+'&redirect_uri='+redirect_url+'&scope='+scope+'&response_type=code'
        return(auth_url)
@ns_client.route('/AccessToken')
class Client(Resource):
    @ns_client.expect(accesstoken_postpraser)
    def post(self):
        payload = api.payload
        client_id = payload['client_id']
        client_secret = payload['client_secret']
        username = payload['username']
        password = payload['password']
        try:
            token = clientAuth.gettoken(client_id,client_secret,username,password)
            return token
        except Exception as e: 
            print(e)
            return e
@ns_client.route('/Token/Validate')
class Client(Resource):
    @ns_client.expect(token_validate_postpraser)
    def post(self):
        payload = api.payload
        accesstoken = payload['access_token']
        verify = clientAuth.get_userinfo(accesstoken)
        try:
            if(verify['error']):
                return False
        except:
            return True
@ns_client.route('/Token/Refresh')
class Client(Resource):
    @ns_client.expect(token_refresh_postpraser)
    def post(self):
        payload = api.payload
        client_id = payload['client_id']
        client_secret = payload['client_secret']
        refresh_token = payload['refresh_token']
        try:
            token = clientAuth.refreshtoken(client_id,client_secret,refresh_token)
            return token
        except Exception as e: 
            print(e)
            return e



if __name__ == '__main__':
    app.run(debug=True)