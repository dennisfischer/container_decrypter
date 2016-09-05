import sys; reload(sys); sys.setdefaultencoding('utf-8')
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework.renderers import JSONRenderer
from rest_framework.parsers import JSONParser
from dlc.models import DLC
from dlc.serializers import DLCSerializer
from dlc import computedlc
import base64
import re


class JSONResponse(HttpResponse):
    """
    An HttpResponse that renders its content into JSON.
    """
    def __init__(self, data, **kwargs):
        content = JSONRenderer().render(data)
        kwargs['content_type'] = 'application/json'
        super(JSONResponse, self).__init__(content, **kwargs)
    
@csrf_exempt
def dlc_list(request):
    """
    List all code snippets, or create a new snippet.
    """
    if request.method == 'GET':
        dlcs = DLC.objects.all;
        dlc = DLC(dlc='foo = "bar"\n')
        serializer = DLCSerializer(dlc)
        return JSONResponse(serializer.data)

    elif request.method == 'POST':
        data = JSONParser().parse(request)
        obj = DLC.objects.filter(dlc=data["dlc"])
        if obj.exists():
            serializer = DLCSerializer(obj[0])
            return JSONResponse(serializer.data, status=200)
        else:
            try:                
                data["links"] = computedlc.decrypt(data["dlc"])
            except:
                e = sys.exc_info()[0]
                serializer = DLCSerializer(data=data)
                return JSONResponse("Error in DLC"+str(e), status=400)

            serializer = DLCSerializer(data=data)
            if serializer.is_valid():            
                serializer.save()
                return JSONResponse(serializer.data, status=201)
            return JSONResponse(serializer.errors, status=400)


@csrf_exempt
def dlc_detail(request, pk):
    """
    Retrieve, update or delete a code snippet.
    """
    try:
        dlc = DLC.objects.get(pk=pk)
    except DLC.DoesNotExist:
        return HttpResponse(status=404)

    if request.method == 'GET':
        serializer = DLCSerializer(dlc)
        return JSONResponse(serializer.data)

    elif request.method == 'PUT':
        data = JSONParser().parse(request)
        serializer = DLCSerializer(dlc, data=data)
        if serializer.is_valid():
            serializer.save()
            return JSONResponse(serializer.data)
        return JSONResponse(serializer.errors, status=400)

    elif request.method == 'DELETE':
        snippet.delete()
        return HttpResponse(status=204)