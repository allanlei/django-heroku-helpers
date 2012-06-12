import base64

from django.http import HttpResponse
from django.contrib.auth import authenticate, login
from django.conf import settings

import datetime
import csv
import logging
import re
import hashlib
import random
import string

reg = re.compile('(\w+)[:=] ?"?(\w+)"?')
opaque = hashlib.sha1(datetime.datetime.now().strftime('%H%d%m%Y')).hexdigest()

def basic(func, realm='', admin_username=getattr(settings, 'ADMIN_LOGIN', None), admin_password=getattr(settings, 'ADMIN_PASSWORD', None)):
    def wrapper(request, *args, **kwargs):
        if admin_username is None:
            return func(request, *args, **kwargs)
        response = HttpResponse(status=401)
        response['WWW-Authenticate'] = 'Basic realm="{realm}"'.format(realm=realm)
        
        if 'HTTP_AUTHORIZATION' in request.META:
            auth_type, credentials = request.META['HTTP_AUTHORIZATION'].split(' ', 1)
            
            if auth_type.lower() == 'basic':
                username, password = base64.b64decode(credentials).split(':')
                
                if username == admin_username and password == admin_password:
                    response = func(request, *args, **kwargs)
        return response
    return wrapper


def digest(func, realm='', admin_username=getattr(settings, 'ADMIN_LOGIN', None), admin_password=getattr(settings, 'ADMIN_PASSWORD', None)):
    def wrapper(request, *args, **kwargs):
        response = HttpResponse(status=401)
        
        response['WWW-Authenticate'] = 'Digest realm="{realm}", nonce="{nonce}", opaque="{opaque}", qop="{qop}"'.format(
            realm=realm, 
            domain=request.path,
            qop='auth,auth-int',
            algorithm='MD5', 
            nonce=hashlib.sha256(datetime.datetime.now().strftime('%Y%m%d%H%M')).hexdigest(), 
            opaque=opaque,         #any string will do, never sent in plain text over the wire
        )
        
        if 'HTTP_AUTHORIZATION' in request.META:
            auth_type, credentials = request.META['HTTP_AUTHORIZATION'].split(' ', 1)
            
            if auth_type.lower() == 'digest':
                creds = dict(reg.findall(credentials))
                
                if creds['opaque'] == opaque and creds['nonce'] == hashlib.sha256(datetime.datetime.now().strftime('%Y%m%d%H%M')).hexdigest():
                    signature = hashlib.md5('{0}:{1}:{2}:{3}:{4}:{5}'.format(
                        get_ha1(realm=realm, username=creds.get('username'), password=admin_password),
                        creds['nonce'],
                        creds.get('nc', ''),
                        creds.get('cnonce', ''),
                        creds.get('qop', ''),
                        get_ha2(method=request.method, path=request.get_full_path()),
                    )).hexdigest()
                    
                    if signature == creds['response']:
                        response = func(request, *args, **kwargs)
        return response
    return wrapper


def get_ha1(realm='', username='', password=''):
    return hashlib.md5('{0}:{1}:{2}'.format(username, realm, password)).hexdigest()

def get_ha2(method='GET', path=''):
    return hashlib.md5('{0}:{1}'.format(method, path)).hexdigest()
