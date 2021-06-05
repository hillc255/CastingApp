import json
from flask import request, _request_ctx_stack
from functools import wraps
from jose import jwt
from urllib.request import urlopen


AUTH0_DOMAIN = 'autumn-voice-0666.us.auth0.com' # heroku auth0 domain
ALGORITHMS = ['RS256']
#API_AUDIENCE = 'cast-app' # heroku app name
#API_AUDIENCE = 'https://cast-app.herokuapp.com/api'
API_AUDIENCE = 'f7ZLU2DmWeRcLuikyEKjqk0893KA2Mbj'


# AuthError Exception
'''
AuthError Exception
A standardized way to communicate auth failure modes
Note: The below code mostly comes from Auth0's Quickstart
Python API: Authorization
'''


class AuthError(Exception):
    def __init__(self, error, status_code):
        self.error = error
        self.status_code = status_code

        print("***Exception complete")


# Auth Header

'''
@TODO implement get_token_auth_header() method
    it should attempt to get the header from the request
        it should raise an AuthError if no header is present
    it should attempt to split bearer and the token
        it should raise an AuthError if the header is malformed
    return the token part of the header
def get_token_auth_header():
   raise Exception('Not Implemented')
'''


def get_token_auth_header():
    """Obtains the Access Token from the Authorization Header
    """

    if 'Authorization' not in request.headers:
        raise AuthError({
         'code': 'authorization_header_missing',
         'description': 'Authorization header is expected.'
        }, 401)

    auth_header = request.headers['Authorization']
    headers_parts = auth_header.split(' ')

    if len(headers_parts) != 2:
        raise AuthError({
         'code': 'invalid_header',
         'description': 'Authorization header must be bearer token.'
        }, 401)

    elif headers_parts[0].lower() != 'bearer':
        raise AuthError({
         'code': 'invalid_header',
         'description': 'Authorization header must start with "Bearer".'
        }, 401)

    return headers_parts[1]

    print("***Headers complete")


'''
@TODO implement check_permissions(permission, payload) method
    @INPUTS
        permission: string permission (i.e. 'post:drink')
        payload: decoded jwt payload
    it should raise an AuthError if permissions are not included in the payload
        !!NOTE check your RBAC settings in Auth0
    it should raise an AuthError if the requested permission string is not in
    the payload permissions array
    return true otherwise
def check_permissions(permission, payload):
    raise Exception('Not Implemented')
'''


def check_permissions(permission, payload):
    if 'permissions' not in payload:
        raise AuthError({
            'code': 'invalid_claims',
            'description': 'Permissions not included in JWT.'
        }, 400)

    if permission not in payload['permissions']:
        raise AuthError({
            'code': 'unauthorized',
            'description': 'Permission not found.'
        }, 403)
    return True

    print("***Permissions complete")

'''
@TODO implement verify_decode_jwt(token) method
    @INPUTS
        token: a json web token (string)
    it should be an Auth0 token with key id (kid)
    it should verify the token using Auth0 /.well-known/jwks.json
    it should decode the payload from the token
    it should validate the claims
    return the decoded payload
    !!NOTE urlopen has a common certificate error described here:
    https://stackoverflow.com/questions/50236117/scraping-ssl-certificate-
    verify-failed-error-for-http-en-wikipedia-org
def verify_decode_jwt(token):
    raise Exception('Not Implemented')
'''


def verify_decode_jwt(token):
    jsonurl = urlopen(f'https://{AUTH0_DOMAIN}/.well-known/jwks.json')
    jwks = json.loads(jsonurl.read())
    print('token= ', token)
    unverified_header = jwt.get_unverified_header(token)
    rsa_key = {}
    if 'kid' not in unverified_header:
        raise AuthError({
            'code': 'invalid_header',
            'description': 'Authorization malformed.'
        }, 401)

    for key in jwks['keys']:
        if key['kid'] == unverified_header['kid']:
            rsa_key = {
                'kty': key['kty'],
                'kid': key['kid'],
                'use': key['use'],
                'n': key['n'],
                'e': key['e']
            }
    if rsa_key:
        try:
            payload = jwt.decode(
                token,
                rsa_key,
                algorithms=ALGORITHMS,
                audience=API_AUDIENCE,
                issuer='https://' + AUTH0_DOMAIN + '/'
            )

            return payload

        except jwt.ExpiredSignatureError:
            raise AuthError({
                'code': 'token_expired',
                'description': 'Token expired.'
            }, 401)

        except jwt.JWTClaimsError:
            raise AuthError({
                'code': 'invalid_claims',
                'description': 'Incorrect claims. Please, check the audience and issuer.'
            }, 401)
        except Exception:
            raise AuthError({
                'code': 'invalid_header',
                'description': 'Unable to parse authentication token.'
            }, 400)
    raise AuthError({
                'code': 'invalid_header',
                'description': 'Unable to find the appropriate key.'
            }, 400)

print("***Decode complete")

'''
@TODO implement @requires_auth(permission) decorator method
    @INPUTS
        permission: string permission (i.e. 'post:drink')
    it should use the get_token_auth_header method to get the token
    it should use the verify_decode_jwt method to decode the jwt
    it should use the check_permissions method validate claims and check
      the requested permission
    return the decorator which passes the decoded payload to the decorated
    method
'''

def requires_auth(permission=''):
    def requires_auth_decorator(f):
        @wraps(f)
        def wrapper(*args, **kwargs):
            jwt = get_token_auth_header()
            payload = verify_decode_jwt(jwt)
            check_permissions(permission, payload)
            return f(payload, *args, **kwargs)
        return wrapper
    return requires_auth_decorator

    print("***Requires_auth complete")

'''
Auth0 Handling Authorization Through Roles
https://auth0.com/blog/using-python-flask-and-angular-to-build-
modern-web-apps-part-3/#Handling-Authorization-Through-Roles

'''
print("***requires_role start")

def requires_role(required_role):
    def decorator(f):
        def wrapper(**args):
            token = get_token_auth_header()
            unverified_claims = jwt.get_unverified_claims(token)
            # search current token for the expected role
            if unverified_claims.get('https://cast-app.herokuapp.com/roles'):
                roles = unverified_claims['https://cast-app.herokuapp.com/roles']
                for role in roles:
                    if role == required_role:
                        return f(**args)

            raise AuthError({
                'code': 'insuficient_roles',
                'description': 'You do not have the roles needed to perform this operation.'
            }, 401)

        # Renaming the function name:
        wrapper.__name__ = f.__name__
        return wrapper

    return decorator

    print("***requires_role complete")
