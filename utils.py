import operator
import re

from django.http import HttpResponseRedirect

def build_ua_filter(pattern, redirect_url, version=None, negate=False, compare=operator.lt, redirect_class=HttpResponseRedirect):
    pattern = re.compile(pattern)
    
    onsuccess, onfailure = None, redirect_class(redirect_url)
    if negate:
        onsuccess, onfailure = onfailure, onsuccess        
        
    def f(ua):
        match = pattern.search(ua.lower())

        if match:
            if version is None:
                return onsuccess
            else:
                if match.groupdict().get('version', None) is not None:
                    ua_version = match.group('version')
                else:
                    ua_version = match.group(1)
                
                if compare(ua_version, str(version)):
                    return onfailure
                return onsuccess
        
        return onfailure
        
    return f
    
    