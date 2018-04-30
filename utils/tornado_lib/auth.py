#!/user/bin/python
#coding=utf8

from requests_oauthlib import OAuth2Session, OAuth1Session
from requests_oauthlib.compliance_fixes import facebook_compliance_fix, linkedin_compliance_fix

import json
try:
    from urlparse import parse_qsl
except ImportError:
    from urllib.parse import parse_qsl

from oauthlib.common import to_unicode
from facebook import GraphAPI
import logging
from dropbox.session import DropboxSession
from dropbox.client import DropboxClient
import unicodedata
import base64

class OAuthBaseMixin(object):
    client_id = None
    client_secret = None
    redirect_uri = None
    authorization_base_url = None
    scopes = []
    token = None


    @property
    def auth_client(self):
        if not hasattr(self, '_auth_client'):
            self._auth_client = self.get_auth_client()
        return self._auth_client

    def get_redirect_uri(self):
        if self.redirect_uri:
            if self.redirect_uri.startswith('http'):
                return self.redirect_uri
            return self.request.protocol + "://" + self.request.host + self.redirect_uri
        return self.request.full_url()

    def get_auth_client(self):
        raise NotImplementedError

    def authorize_redirect(self, **extra_params):
        auth_client = self.get_auth_client()

        authorization_url, state = auth_client.authorization_url(self.authorization_base_url, **extra_params) 
            #access_type="offline", approval_prompt="force")
        logging.info(authorization_url)
        self.redirect(authorization_url)



class OAuth1BaseMixin(OAuthBaseMixin):
    request_token_url = None
    access_token_url = None

    def get_authenticated_token(self, **kwargs):
        self.auth_client._populate_attributes(self.session)
        self.auth_client.parse_authorization_response(self.request.full_url())
        self.auth_client._client.client.verifier = self.get_argument('uid', None)
        self.token = self.auth_client.fetch_access_token(self.access_token_url)
        return self.token

    def authorize_redirect(self, **extra_params):
        auth_client = self.get_auth_client()
        request_token = auth_client.fetch_request_token(self.request_token_url)
        self.session['oauth_token'] = request_token['oauth_token']
        self.session['oauth_token_secret'] = request_token['oauth_token_secret']

        authorization_url = auth_client.authorization_url(self.authorization_base_url, **extra_params) 
            #access_type="offline", approval_prompt="force")
        logging.info(authorization_url)
        self.redirect(authorization_url)

    def get_auth_client(self):
        _auth_client = OAuth1Session(self.client_id, self.client_secret, callback_uri=self.get_redirect_uri())
        return _auth_client

class OAuth2BaseMixin(OAuthBaseMixin):
    token_url = None
    user_info_url = None
    
    def get_authenticated_token(self, **kwargs):
        token = self.auth_client.fetch_token(self.token_url, client_secret=self.client_secret,  authorization_response=self.request.full_url(), **kwargs)
        self.token = token
        return token

    def get_authenticated_user(self):
        return self.auth_client.get(self.user_info_url)

    def get_auth_client(self):
        return OAuth2Session(self.client_id, scope=self.scopes, redirect_uri=self.get_redirect_uri())


class GoogleOAuthMixin(OAuth2BaseMixin):
    authorization_base_url = "https://accounts.google.com/o/oauth2/auth"
    token_url = "https://accounts.google.com/o/oauth2/token"
    
    scopes = [
        "https://www.googleapis.com/auth/userinfo.email",
        "https://www.googleapis.com/auth/userinfo.profile"
    ]
    user_info_url = 'https://www.googleapis.com/oauth2/v1/userinfo'

    def _jwt_decode(self, input_jwt):
        NORMAL_FORM = 'NFKD'
        try:
            input_jwt = unicodedata.normalize(NORMAL_FORM, input_jwt).encode(
                'ascii', 'ignore')
            # Append extra characters to make original string base 64 decodable.
            input_jwt += '=' * (4 - (len(input_jwt) % 4))
            decoded_jwt = base64.urlsafe_b64decode(input_jwt)
        except:
            return None
        else:
            decoded_jwt = json.loads(decoded_jwt)
            return decoded_jwt

    def decode_id_token(self, data):
        input_dwts = data.split('.')
        header = self._jwt_decode(input_dwts[0])
        claims = self._jwt_decode(input_dwts[1])
        return header, claims


class FacebookOAuthMixin(OAuth2BaseMixin):
    authorization_base_url = 'https://www.facebook.com/dialog/oauth'
    token_url = 'https://graph.facebook.com/oauth/access_token'
    user_info_url = 'https://graph.facebook.com/me'

    def get_userinfo(self):
        """
        {'first_name': u'\u5e86\u521b', 'last_name': u'\u66fe', 'verified': True, 'name': u'\u66fe\u5e86\u521b', 'locale': 'en_US', 'updated_time': '2014-03-03T13:40:22+0000', 'birthday': '12/22/1981', 'link': 'https://www.facebook.com/profile.php?id=1391650404', 'timezone': 8, 'id': '1391650404'}
        """
        fb_api = GraphAPI(self.token['access_token'])
        try:
            res = fb_api.get_object('me')
            return res
        except Exception, e:
            logging.warning("facebook query info fail %s", e, exc_info=True)
            return None

    def get_auth_client(self):
        _auth_client = OAuth2Session(self.client_id, scope=self.scopes, redirect_uri=self.get_redirect_uri())
        _auth_client = facebook_compliance_fix(_auth_client)
        return _auth_client


class LinkedinOAuthMixin(OAuth2BaseMixin):
    authorization_base_url = 'https://www.linkedin.com/uas/oauth2/authorization'
    token_url = 'https://www.linkedin.com/uas/oauth2/accessToken'
    user_info_url = 'https://api.linkedin.com/v1/people/~'

    def get_auth_client(self):
        _auth_client = OAuth2Session(self.client_id, scope=self.scopes, redirect_uri=self.get_redirect_uri())
        _auth_client = linkedin_compliance_fix(_auth_client)
        return _auth_client


class LinkedinOAuthMixin(OAuth1BaseMixin):
    authorization_base_url = 'https://api.linkedin.com/uas/oauth/authenticate'
    request_token_url = 'https://api.linkedin.com/uas/oauth/requestToken'
    access_token_url = 'https://api.linkedin.com/uas/oauth/accessToken'

    def get_authenticated_token(self, **kwargs):
        self.auth_client._populate_attributes(self.session)
        self.auth_client.parse_authorization_response(self.request.full_url())
        self.auth_client._client.client.verifier = self.get_argument('oauth_verifier', None)
        self.token = self.auth_client.fetch_access_token(self.access_token_url)
        return self.token



class TwitterOAuthMixin(OAuth1BaseMixin):
    authorization_base_url = 'https://api.twitter.com/oauth/authorize'
    request_token_url = 'https://api.twitter.com/oauth/request_token'
    access_token_url = 'https://api.twitter.com/oauth/access_token'


def instagram_compliance_fix(session):

    def _compliance_fix(r):
        token = r.json()
        expires = token.get('expires')
        if expires is not None:
            token['expires_in'] = expires
        token['token_type'] = 'Bearer'
        r._content = to_unicode(json.dumps(token)).encode('UTF-8')
        return r

    session.register_compliance_hook('access_token_response', _compliance_fix)
    return session


class InstagramOAuthMixin(OAuth2BaseMixin):
    authorization_base_url = 'https://api.instagram.com/oauth/authorize/'
    token_url = 'https://api.instagram.com/oauth/access_token'

    def get_auth_client(self):
        _auth_client = OAuth2Session(self.client_id, scope=self.scopes, redirect_uri=self.get_redirect_uri())
        _auth_client = instagram_compliance_fix(_auth_client)
        return _auth_client


#class DropboxOAuthMixin(OAuth2BaseMixin):
#    authorization_base_url = 'https://www.dropbox.com/1/oauth2/authorize'
#    token_url = 'https://api.dropbox.com/1/oauth2/token'

class DropboxOAuthMixin(OAuth1BaseMixin):
    authorization_base_url = 'https://www.dropbox.com/1/oauth/authorize'
    access_token_url = 'https://api.dropbox.com/1/oauth/access_token'
    request_token_url = 'https://api.dropbox.com/1/oauth/request_token'
    ACCESS_TYPE = 'app_folder'

    def get_authenticated_token(self, **kwargs):
        self.auth_client._populate_attributes(self.session)
        self.auth_client.parse_authorization_response(self.request.full_url())
        self.auth_client._client.client.verifier = self.get_argument('uid', None)
        self.token = self.auth_client.fetch_access_token(self.access_token_url)
        return self.token

    def get_userinfo(self):
        """
        {u'referral_link': u'https://db.tt/LbG4aSx1', u'display_name': u'waiting easilydo', u'uid': 330936854, u'country': u'HK', u'email': u'waiting@easilydo.com', u'team': None, u'quota_info': {u'datastores': 0, u'shared': 0, u'quota': 2147483648, u'normal': 363213}}
        """
        sess = DropboxSession(self.client_id, self.client_secret, self.ACCESS_TYPE)
        sess.set_token(self.token['oauth_token'], self.token['oauth_token_secret'])

        api = DropboxClient(sess)
        try:
            res = api.account_info()
            return res
        except Exception, e:
            logging.warning("dropbox query info fail %s", e, exc_info=True)
            return None



class EvernoteOAuthMixin(OAuth1BaseMixin):
    authorization_base_url = 'https://www.evernote.com/OAuth.action'
    access_token_url = 'https://www.evernote.com/oauth'
    request_token_url = 'https://www.evernote.com/oauth'

class SandboxEvernoteOAuthMixin(OAuth1BaseMixin):
    authorization_base_url = 'https://sandbox.evernote.com/OAuth.action'
    access_token_url = 'https://sandbox.evernote.com/oauth'
    request_token_url = 'https://sandbox.evernote.com/oauth'

EvernoteOAuthMixin = SandboxEvernoteOAuthMixin

class BoxOAuthMixin(OAuth2BaseMixin):
    authorization_base_url = 'https://app.box.com/api/oauth2/authorize'
    token_url = 'https://app.box.com/api/oauth2/token'


class SalesforceOAuthMixin(OAuth2BaseMixin):
    authorization_base_url = 'https://login.salesforce.com/services/oauth2/authorize'
    token_url = 'https://login.salesforce.com/services/oauth2/token'


class YahooOAuthMixin(OAuth1BaseMixin):
    access_token_url = 'https://api.login.yahoo.com/oauth/v2/get_token'
    authorization_base_url = 'https://api.login.yahoo.com/oauth/v2/request_auth'
    request_token_url = 'https://api.login.yahoo.com/oauth/v2/get_request_token'
    
