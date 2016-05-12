# -*- coding: utf-8 -*-
import base64

from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse
from django.conf import settings
from django.contrib.auth import authenticate, login
from django.template import RequestContext
from django.contrib.auth.models import User
from django.core.cache import cache
from django.core.files.base import ContentFile
from requests.utils import quote

from .forms import TopicForm
from .models import Topic, Poll



@login_required(redirect_field_name=None)
def main(request):
    return render(request, 'voting/main.html')


@login_required(redirect_field_name=None)
@csrf_exempt
def up(request):
    #topic = Topic.objects.filter(user=request.user)
    #if topic.exists():
    #    return JsonResponse({"ret": 2})

    form = TopicForm(request.POST)
    if request.method == 'POST':
        if form.is_valid():
            m = form.save(commit=False)
            m.user = request.user
            fdata = request.POST.get('photo', "")
            m.photo.save("%d.jpg" % m.user.id, ContentFile(base64.b64decode(fdata)), save=False)
            m.save()
            return JsonResponse({"ret": 0})
    return JsonResponse({"ret": 1})


@login_required(redirect_field_name=None)
def detail(request, topic_id):
    topic = get_object_or_404(Topic, pk = topic_id)
    user = topic.user
    return JsonResponse({"name": user.last_name,
                         "url": topic.photo.url,
                         "id": topic.id,
                         "ranking": topic.ranking(),
                         "polls": topic.polls})


@login_required(redirect_field_name=None)
def vote(request, topic_id):
    topic = get_object_or_404(Topic, pk = topic_id)
    if not Poll.objects.filter(user=request.user).exists():
        Poll.objects.create(user=request.user, topic = topic)
        topic.polls += 1
        topic.save()
        return JsonResponse({"ret": 0})
    return JsonResponse({"ret": 2})



@login_required(redirect_field_name=None)
def uploaded(request):
    ret = Topic.objects.filter(user=request.user).exists()
    return JsonResponse({"ret": int(ret)}, safe=False)


def get_sorted_list(kind, offset=0, limit=9):
    order_key = "-polls"
    if kind == "new":
        order_key = "-ctime"
    topic_list = Topic.objects.all().order_by(order_key)[int(offset):int(limit) + int(offset)]
    return topic_list


@login_required(redirect_field_name=None)
def pullboard(requests, kind, offset, limit):
    topic_list = get_sorted_list(kind, offset, limit)
    lt = [{"id": topic.id,
           "url": topic.photo.url,
            "polls": topic.polls,
            "headimgurl": topic.user.email,
            "ranking": topic.ranking() if kind=="hot" else idx+1}\
            for idx, topic in enumerate(topic_list)]
    return JsonResponse(lt, safe=False)


# callback entry
def zumbalogin(request):
    openId = request.GET.get("openId")
    state = request.GET.get("state")

    rep = auth_and_login(request, openId)
    if rep is True:
        return HttpResponseRedirect(reverse('main'))
    return rep


def auth_and_login(request, openId):
    user = authenticate(openId=openId)
    if user is None:
        return HttpResponse("登陆失败")

    login(request, user)
    return True

