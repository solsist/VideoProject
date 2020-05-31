# coding:utf-8

from django.views.generic import View
from app.libs.base_render import render_to_response
from app.model.auth import ClientUser


class UserView(View):
    TEMPLATE = 'dashboard/user.html'

    def get(self, request):
        users = ClientUser.objects.all()
        data = {'users': users}

        return render_to_response(request, self.TEMPLATE, data=data)


class UserStatus(View):
    TEMPLATE = 'dashboard/user.html'

    def get(self, request, user_id):
        print(user_id)
        user = ClientUser.objects.get(pk=user_id)
        user.status = not user.status
        user.save()
        users = ClientUser.objects.all()
        data = {'users': users}
        return render_to_response(request, self.TEMPLATE, data=data)
