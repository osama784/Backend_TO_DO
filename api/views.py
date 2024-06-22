from rest_framework.response import Response
from rest_framework.decorators import api_view


@api_view(['GET'])
def getRoutes(request):
    routes = [
        {'GET': 'tasks/'},
        {'POST': 'tasks/create/'},
        {'PUT': 'tasks/<int:pk>/update/'},
        {'DELETE': 'tasks/<int:pk>/delete/'}
    ]

    return Response(routes)
