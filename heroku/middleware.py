from django.http import HttpResponseRedirect
from django.conf import settings


class SecureReverseProxyMiddleware(object):
    def process_request(self, request, *args, **kwargs):
        if not request.is_secure():
            is_secure = lambda: False
            
            requirements = dict(settings.SECURE_PROXY_SSL_HEADER)
            for header, value in requirements.items():
                if header in request.META:
                    if value is None or request.META[header] == value:
                        requirements.pop(header)

            if not requirements:
                is_secure = lambda: True
                
            request.is_secure = is_secure
        return None

class HttpsRedirectMiddleware(object):
    def process_request(self, request, *args, **kwargs):
        if not request.is_secure():
            return HttpResponseRedirect('https://{host}{path}'.format(host=request.get_host(), path=request.get_full_path()))
        return None
