from django.http import HttpResponse, HttpResponseNotFound, HttpRequest


def course(request: HttpRequest, name: str = ''):
    # Get class state if exists, else do a search
    if request.method == 'GET':
        pass
    # Modify class state
    elif request.method == 'POST':
        pass
    # Create a class
    elif request.method == 'PUT':
        pass
    # Delete a class
    elif request.method == 'DELETE':
        pass
    return HttpResponseNotFound()
