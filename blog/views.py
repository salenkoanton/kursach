from django.shortcuts import render

# Create your views here.
from django.shortcuts import render
import json
from django.forms.models import modelform_factory
from django.views.generic import View
from user.models import User, Author, Image
from .models import Post, Comment
import sys
from django.http import HttpResponse

def main(request) :
    return render(request, "index.html", {})

def bla(request):
    if request.method == "GET":
        return render(request, "bla.html", {})
    elif request.method == "POST":
        print(request.body)
        blabla = request.body.decode('utf-8')
        params = dict([p.split('=') for p in blabla.split('&')])
        print(params)
        print (params['login'])
        User.objects.create(login = params['login'], password = params['password'], nickname = params['nickname'])
        return render(request, "bla.html", {})
def passport(request):
    if request.method == "GET":
        return render(request, "blabla.html", {})
    elif request.method == "POST":
        print(request.body)

        return render(request, "blabla.html", {})

def prods(request):
    response_data = []
    for p in SaleProduct.objects.all():
        response_data.append(p.dict())
    print(response_data)
    return HttpResponse(json.dumps(response_data), content_type="application/json")

class prods_id(View):
    def get(self, request, path):
        try:
            response_data = SaleProduct.objects.get(id=int(path)).dict()
        except SaleProduct.DoesNotExist:
            return HttpResponse(json.dumps({'error massage' : 'wrong id'}), content_type="application/json")
        except:
            print("Unexpected error:", sys.exc_info())
            return HttpResponse(json.dumps({'error massage': 'server error'}), content_type="application/json")
        print(response_data)
        return HttpResponse(json.dumps(response_data), content_type="application/json")

    def delete(self, request, path):
        try:
            elem = SaleProduct.objects.get(id=int(path))
            response_data = elem.dict()
            elem.delete()
        except SaleProduct.DoesNotExist:
            return HttpResponse(json.dumps({'error massage' : 'wrong id'}), content_type="application/json")
        except:
            print("Unexpected error:", sys.exc_info())
            return HttpResponse(json.dumps({'error massage': 'server error'}), content_type="application/json")
        print(response_data)
        return HttpResponse(json.dumps(response_data), content_type="application/json")