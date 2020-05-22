# coding:utf-8

from django.views.generic import View
from django.http import JsonResponse
from app.model.comment import CommentView
from app.model.auth import ClientUser
from app.model.video import Videos


class Comment(View):

    def post(self, request):
        content = request.POST.get('content', '')
        user_id = request.POST.get('userId', '')
        video_id = request.POST.get('videoId', '')
        if not all([content, user_id, video_id]):
            return JsonResponse({'code': -1, 'msg': '缺少必要字段'})

        video = Videos.objects.get(pk=video_id)
        user = ClientUser.objects.get(pk=user_id)

        comment = CommentView.objects.create(content=content, video=video, user=user)
        data = {'comment': comment.data()}
        return JsonResponse({'code': 0, 'msg': 'success', 'data': data})
