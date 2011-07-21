from django.http import HttpResponse

def index(request):
    return HttpResponse('Hello World!')

def unsupported(request):
    return HttpResponse('Your browser is not supported :(')