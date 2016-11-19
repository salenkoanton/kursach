# Create your views here.
from django.shortcuts import render
import json
from django.forms.models import modelform_factory
from django.views.generic import View
from .models import User, Image, Author
from blog.models import Post, Comment
from audio.models import Audio
import sys
from django.http import HttpResponse
from django.contrib.auth.models import User as DJangoUser
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, authenticate
from django.contrib.auth import logout as djlogout
from django.shortcuts import redirect
from django.utils.decorators import method_decorator


class Users_id(View):
    @method_decorator(login_required(login_url='/login/'))
    def get(self, request, path):
        try:
            response_data = User.objects.get(id=int(path)).dict()
        except User.DoesNotExist:
            return HttpResponse(json.dumps({'error massage': 'wrong id'}), content_type="application/json")
        except:
            print("Unexpected error:", sys.exc_info())
            return HttpResponse(json.dumps({'error massage': 'server error'}), content_type="application/json")
        print(response_data)
        return HttpResponse(json.dumps(response_data), content_type="application/json")

    @method_decorator(login_required(login_url='/login/'))
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
    @method_decorator(login_required(login_url='/login/'))
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

    @method_decorator(login_required(login_url='/login/'))
    def post(self, request, path):
        params_to_parse = request.META['QUERY_STRING']
        params = dict([p.split('=') for p in params_to_parse.split('&')])
        try:
            print(params)
            Post.objects.create(text=params['text'], creator=User.objects.get(id=int(params['creator'])),
                                owner=User.objects.get(id=int(path)))
        except:
            print('not post post')
            print("Unexpected error:", sys.exc_info())
        return self.get(request, path)


class Users_id_followers(View):
    @method_decorator(login_required(login_url='/login/'))
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


@login_required(login_url='/login/')
def users(request):
    try:
        response_data = [i.dict() for i in User.objects.all()]
    except:
        print("Unexpected error:", sys.exc_info())
        return HttpResponse(json.dumps({'error massage': 'server error'}), content_type="application/json")
    print(response_data)
    return HttpResponse(json.dumps(response_data), content_type="application/json")


class Logout(View):
    def get(self, request):
        djlogout(request)
        return redirect('/login/')


class Login(View):
    def get(self, request):
        return render(request, 'login.html', {})

    def post(self, request):
        params = request.POST
        print(params['email'])
        if params['email'].find('@') == -1:
            username = params['email']
        else:
            try:
                username = User.objects.get(djangoUser__email=params['email']).djangoUser.username
            except:
                print('error')
                username = None
                return render(request, 'login.html', {})
        user = authenticate(username=username, password=params['password'])
        if user is not None:
            if user.is_active:
                login(request, user)
                try:
                    print(request.GET['next'])
                    return redirect(request.GET['next'])
                except:
                    return redirect('/blog/' + str(user.customUser.id) + '/wall')
            else:
                return HttpResponse(json.dumps({'login': 'error disabled'}), content_type="application/json")
        else:
            return HttpResponse(json.dumps({'login': "error pass don't manch"}), content_type="application/json")


def auth(request):
    if request.method == 'GET':
        return render(request, 'auth.html', {})
    elif request.method == 'POST':
        params = request.POST
        print(params.keys())
        try:
            try:
                user = DJangoUser.objects.get(username=params['username'])
                if user is not None:
                    return render(request, 'auth.html', {'error': 'Error, we already have a user with such name'})
            except:
                print(params)
                try:
                    print(params['email'])
                    user = DJangoUser.objects.get(email=params['email'])
                    print(user)
                    if user is not None:
                        return render(request, 'auth.html', {'error': 'Error, we already have a user with such email'})
                except:
                    print(sys.exc_info())
                    print('success')
            user = DJangoUser.objects.create_user(params['username'], params['email'], params['password'])
            user.last_name = params['lastname']
            user.first_name = params['firstname'];
            user.save()
            cus_us = User.objects.create(djangoUser=user, birthdate=params['birthdate'])
            if params['sex'] == 'male':
                cus_us.sex = True
                cus_us.avatar = User.MALE_AVATAR
            else:
                cus_us.sex = False
                cus_us.avatar = User.FEMALE_AVATAR
            cus_us.save()
        except ValueError:
            params = {}
        print(params)
        return render(request, 'auth.html', {'error': 'Invalid input'})


def main(request):
    return render(request, "main.html", {request})


class Author_id(View):
    def get(self, request, path):
        if request.user.is_authenticated():
            you = request.user.customUser
        else:
            you = None
        a = Author.objects.get(id=int(path))
        return render(request, "author.html", {'author': a, 'you': you})


    def post(self, request, path):
        user = request.user
        params = request.POST
        try:
            user.customUser.audio.add(Audio.objects.get(id=int(params['add'])))
        except:
            print("Unexpected error:", sys.exc_info())
        return self.get(request, path)

def authors(request):
    if request.user.is_authenticated():
        you = request.user.customUser;
    else:
        you = None
    a = Author.objects.all().order_by('name')
    return render(request, "all.html", {'authors': a, 'you': you})
