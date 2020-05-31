# coding:utf-8

from django.views.generic import View
from django.shortcuts import redirect, reverse
from django.http import JsonResponse
from app.libs.base_render import render_to_response
from app.utils.permission import client_auth
from app.utils.consts import COOKIE_NAME
from app.models import ClientUser
from app.model.auth import hash_password
from app.utils.common import handle_image

class User(View):
    TEMPLATE = 'client/auth/user.html'

    def get(self, request):
        user = client_auth(request)
        data = {'user': user}
        print(user)
        return render_to_response(request, self.TEMPLATE, data=data)

    def post(self, request):
        username = request.POST.get('username')
        password = request.POST.get('password')

        if not all([username, password]):
            error = '缺少必要字段'
            return JsonResponse({'code': -1, 'msg': error})
        user = ClientUser.get_user(username, password)

        if not user:
            error = '用户名或者密码错误，未找到该用户'
            return JsonResponse({'code': -1, 'msg': error})

        if not user.status:
            error = '该用户已注销无法登录'
            return JsonResponse({'code': -1, 'msg': error})

        response = render_to_response(request, self.TEMPLATE)
        response.set_cookie(COOKIE_NAME, str(user.id))
        return response


class Regist(View):

    def post(self, request):
        username = request.POST.get('username', '')
        password = request.POST.get('password', '')

        if not all([username, password]):
            error = '缺少必要字段！'
            return JsonResponse({'code': -1, 'msg': error})
        user = ClientUser.get_user(username, password)
        exists = ClientUser.objects.filter(username=username).exists()

        if exists:
            if not user.status:
                error = '该用户已注销，无法注册！'
                return JsonResponse({'code': -1, 'msg': error})
            error = '该用户名已存在!'
            return JsonResponse({'code': -1, 'msg': error})

        ClientUser.add(username=username, password=password)
        return JsonResponse({'code': 0, 'msg': '注册成功，请您登录'})


class Logout(View):

    TEMPLATE = 'client/auth/user.html'

    def get(self, request):
        response = render_to_response(request, self.TEMPLATE)
        response.set_cookie(COOKIE_NAME, '')
        return response


class ModifyInfo(View):
    TEMPLATE = 'client/auth/userinfo.html'

    def get(self, request, user_id):
        person = ClientUser.objects.filter(pk=user_id)
        data = {'person': person}
        return render_to_response(request, self.TEMPLATE, data=data)

    def post(self, request, user_id):
        password = request.POST.get('password')
        birthday = request.POST.get('birthday')
        gender = request.POST.get('gender')
        url = request.FILES.get('image')
        if not url:
            user = ClientUser.objects.get(pk=user_id)
            try:
                user.password = hash_password(password)
                user.birthday = birthday
                user.gender = gender
                user.save()
            except:
                return False
        else:
            handle_image(url, user_id)
        return redirect(reverse('client_auth'))

class Logoff(View):

    TEMPLATE = 'client/auth/user.html'

    def get(self, request):
        user = client_auth(request)
        response = render_to_response(request, self.TEMPLATE)
        response.set_cookie(COOKIE_NAME, '')
        user.status = False
        user.save()
        return response


