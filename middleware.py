from utils import *

class BrowserFilterMiddleware:

    def __init__(self):
    
        import settings
        
        rules = settings.BROWSER_DETECTION_RULES
        self.ua_filters = []
        self.redirect_urls = set()
        
        for r in rules:
            if hasattr(r[0], '__call__'):
                ua_filter_function = r[0](*r[1:])
            else:
                ua_filter_function = build_ua_filter(*r)
                
            self.ua_filters.append(ua_filter_function)
            self.redirect_urls.add(str(r[1]))

    def process_request(self, request):
        # check whther in redirected url
        if request.path in self.redirect_urls or (request.path + '/') in self.redirect_urls:
            return None
        
        for f in self.ua_filters:
            response = f(request.META['HTTP_USER_AGENT'])
            if response is True:
                return None
            elif response is not None:
                return response
            
        return None