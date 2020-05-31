# coding:utf-8

import os
import time
import shutil
from django.conf import settings
from django.core.files.storage import default_storage
from django.core.files.base import ContentFile
from app.model.video import Videos, VideoSub
from app.tasks.videotask import video_task
from app.model.auth import ClientUser
from app.libs.base_qiniu import video_qiniu
import app.utils.circle_image as circle


def check_and_get_video_type(type_obj, type_value, message):
    try:
        type_obj(type_value)
    except:
        return {'code': -1, 'msg': message}
    return {'code': 0, 'msg': 'success'}


def remove_path(paths):
    for path in paths:
        if os.path.exists(path):
            os.remove(path)


def handle_video(video_file, video_id, number):
    in_path = os.path.join(settings.BASE_DIR, 'app\\dashboard\\temp_in')
    out_path = os.path.join(settings.BASE_DIR, 'app\\dashboard\\temp_out')
    name = '{}_{}'.format(int(time.time()), video_file.name)
    path_name = '\\'.join([in_path, name])

    temp_path = video_file.temporary_file_path()

    shutil.copyfile(temp_path, path_name)

    out_name = '{}_{}'.format(int(time.time()), video_file.name.split('.')[0])
    out_path = '\\'.join([out_path, out_name])
    command = 'ffmpeg -i {} -c copy {}.mp4'.format(path_name, out_path)
    video = Videos.objects.get(pk=video_id)
    video_sub = VideoSub.objects.create(
        video=video,
        url='',
        number=number
    )
    video_task.delay(command, out_path, path_name, video_file.name, video_sub.id)
    return False


def handle_image(image_file, user_id):
    origin_path = os.path.join(settings.BASE_DIR, 'app\\dashboard\\temp_origin')
    in_path = os.path.join(settings.BASE_DIR, 'app\\dashboard\\temp_in')
    out_path = os.path.join(settings.BASE_DIR, 'app\\dashboard\\temp_out')
    image_time = str(int(time.time()))
    origin_image_path = default_storage.save(origin_path+'\\'+image_time+'_'+image_file.name, ContentFile(image_file.read()))
    image_file_name = circle.circle_image(in_path, origin_image_path)

    path = in_path+'\\'+image_file_name
    out_name = '{}_{}'.format(image_time, image_file.name.split('.')[0])
    out_path = '\\'.join([out_path, out_name])
    out_name = '.'.join([out_path, 'png'])
    command = 'ffmpeg -i {} -c copy {}.png'.format(path, out_path)
    os.system(command)
    if not os.path.exists(out_name):
        remove_path([out_name, path, origin_image_path])
        return False
    avatar = video_qiniu.put(image_file_name, out_name)
    if avatar:
        user = ClientUser.objects.get(pk=user_id)
        user.avatar = avatar
        user.save()
        remove_path([out_name, path, origin_image_path])
    remove_path([out_name, path, origin_image_path])
    return False




