import operator
import re

from django.http import HttpResponseRedirect

def _mozilla(redirect_url, version=None, negate=False):
    def f(ua):
        ua = ua.lower()
        match = re.match(r'mozilla(?:.*? rv:([\w.]+))?', ua)

        if 'compatible' not in ua and 'safari' not in ua and 'chrome' not in ua and 'webkit' not in ua and match:
            if version is None or match.group(1) < str(version):
                return HttpResponseRedirect(redirect_url)
                
        return None
    
    return f

MOZILLA = _mozilla
WEBKIT = r'webkit[ \/]([\w.]+)'
OPERA = r'opera(?:.*version)?[ \/]([\w.]+)'
IE = r'msie ([\w.]+)'

def build_ua_filter(pattern, redirect_url, version=None, negate=False, compare=operator.ge, redirect_class=HttpResponseRedirect):
    pattern = re.compile(pattern)
    
    onsuccess, onfailure = None, redirect_class(redirect_url)
    if negate:
        onsuccess, onfailure = onfailure, onsuccess        
        
    def f(ua):
        match = pattern.search(ua.lower())

        if match:
            if version is not None:
                if match.groupdict().get('version', None) is not None:
                    ua_version = match.group('version')
                else:
                    ua_version = match.group(1)
                
                if compare(ua_version, str(version)):
                    return onsuccess

            return onfailure
        
        return None
        
    return f
    

    
    