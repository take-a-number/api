from django.http import HttpResponse, HttpResponseNotFound, HttpRequest


def course(request: HttpRequest, name: str = ''):
    return HttpResponseNotFound()
