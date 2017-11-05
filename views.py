from django.shortcuts import render
from django.shortcuts import render
from django.shortcuts import render_to_response,redirect
from django.template.context_processors import csrf
import json
import requests
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from CH.forms import RequestForm
import pprint
# Create your views here.
def main(request):
    def get_clickhouse_data(query,host,connection_timeout=1500):
        """Метод для обращения к базе данных CH"""
        r=requests.post(host,params={'query':query},timeout=connection_timeout)
        return r.text
    if request.method=='POST':

        return JsonResponse(json.dumps(),safe=False)
    else:
        args={}
        return render_to_response('magazine.html',args={})