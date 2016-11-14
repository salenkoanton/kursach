# Create your views here.
from django.shortcuts import render
import json
from django.forms.models import modelform_factory
from django.views.generic import View
from .models import User
from blog.models import Post, Comment
import sys
from django.http import HttpResponse

class Users_id(View):
    def get(self, request, path):
        try:
            response_data = User.objects.get(id=int(path)).dict()
        except User.DoesNotExist:
            return HttpResponse(json.dumps({'error massage' : 'wrong id'}), content_type="application/json")
        except:
            print("Unexpected error:", sys.exc_info())
            return HttpResponse(json.dumps({'error massage': 'server error'}), content_type="application/json")
        print(response_data)
        return HttpResponse(json.dumps(response_data), content_type="application/json")
    def post(self, request, path):
        params_to_parse = request.META['QUERY_STRING']
        print(request.get_full_path())
        params = dict([p.split('=') for p in params_to_parse.split('&')])
        try:
            print(params['follow'])
            User.objects.get(id=int(path)).follow(params['follow'])
        except:
            print('not follow')
        return self.get(request, path)
class Users_id_wall(View):
    def get(self, request, path):
        try:
            response_data = [i.dict() for i in User.objects.get(id=int(path)).posts.all()]
        except User.DoesNotExist:
            return HttpResponse(json.dumps({'error massage': 'wrong id'}), content_type="application/json")
        except:
            print("Unexpected error:", sys.exc_info())
            return HttpResponse(json.dumps({'error massage': 'server error'}), content_type="application/json")
        print(response_data)
        return HttpResponse(json.dumps(response_data), content_type="application/json")
    def post(self, request, path):
        params_to_parse = request.META['QUERY_STRING']
        params = dict([p.split('=') for p in params_to_parse.split('&')])
        try:
            print(params)
            Post.objects.create(text=params['text'], creator=User.objects.get(id=int(params['creator'])))
        except:
            print('not post post')
            print("Unexpected error:", sys.exc_info())
        return self.get(request, path)




class Users_id_followers(View):
    def get(self, request, path):
        try:
            response_data = [i.dict() for i in User.objects.get(id=int(path)).followers.all()]
        except User.DoesNotExist:
            return HttpResponse(json.dumps({'error massage': 'wrong id'}), content_type="application/json")
        except:
            print("Unexpected error:", sys.exc_info())
            return HttpResponse(json.dumps({'error massage': 'server error'}), content_type="application/json")
        print(response_data)
        return HttpResponse(json.dumps(response_data), content_type="application/json")

def users(request):
    try:
        response_data = [i.dict() for i in User.objects.all()]
    except:
        print("Unexpected error:", sys.exc_info())
        return HttpResponse(json.dumps({'error massage': 'server error'}), content_type="application/json")
    print(response_data)
    return HttpResponse(json.dumps(response_data), content_type="application/json")