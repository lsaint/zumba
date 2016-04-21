# -*- coding: utf-8 -*-
import base64

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
from .models import Topic



@login_required(redirect_field_name=None)
def index(request):
    topic = Topic.objects.filter(user=request.user)
    if topic.exists():
        return HttpResponseRedirect(reverse('detail', kwargs={"topic_id": "%d" % topic[0].id}))

    form = TopicForm(request.POST)
    if request.method == 'POST':
        if form.is_valid():
            m = form.save(commit=False)
            m.user = request.user
            fdata = request.POST.get('photo', "")
            m.photo.save("%d.jpg" % m.user.id, ContentFile(base64.b64decode(fdata)), save=False)
            m.save()
            return HttpResponseRedirect(reverse('leaderboard', kwargs={"kind": "hot"}))

    context = {"form": form}
    return render(request, 'voting/index.html', context)


@login_required(redirect_field_name=None)
def detail(request, topic_id):
    topic = get_object_or_404(Topic, pk = topic_id)
    user = topic.user
    return render(request, 'voting/detail.html', {'topic': topic, "name": user.last_name})


@login_required(redirect_field_name=None)
def vote(request, topic_id):
    topic = get_object_or_404(Topic, pk = topic_id)
    p, created = Poll.objects.get_or_create(user=request.user, topic = topic)
    if created:
        topic.polls += 1
        topic.save()
    return render(request, 'voting/detail.html', {'topic': topic})


@login_required(redirect_field_name=None)
def leaderboard(request, kind):
    topic_list = get_sorted_list(kind)
    return render(request, 'voting/leaderboard.html', {"topic_list": topic_list})


@login_required(redirect_field_name=None)
def uploaded(request):
    ret = Topic.objects.filter(user=request.user).exists()
    return JsonResponse(ret, safe=False)



def get_sorted_list(kind, offset=0, limit=9):
    order_key = "-polls"
    if kind == "new":
        order_key = "-ctime"
    topic_list = Topic.objects.all().order_by(order_key)[int(offset):int(limit) + int(offset)]
    # uids = [x.uid for x in topic_list]
    # users = User.objects.filter(id__in=uids).in_bulk(uids)
    # urls, topic_list = [], list(topic_list)
    # for topic in topic_list[:]:
        # u = users.get(topic.uid)
        # if not u:
            # topic_list.remove(topic)
        # else:
            # urls.append(u.email)
    # topic_list = list(zip(topic_list, urls))
    return topic_list


@login_required(redirect_field_name=None)
def pullboard(requests, kind, offset, limit):
    topic_list = get_sorted_list(kind, offset, limit)
    lt = [(topic.id, topic.photo.url, topic.polls, topic.user.email, topic.ranking())\
            for topic in topic_list]
    return JsonResponse(lt, safe=False)


# callback entry
def zumbalogin(request):
    openId = request.GET.get("openId")
    state = request.GET.get("state")

    rep = auth_and_longin(request, openId)
    if rep is True:
        return HttpResponseRedirect(reverse('leaderboard', kwargs={"kind": "hot"}))
    return rep


def auth_and_longin(request, openId):
    user = authenticate(openId)
    if user is None:
        return HttpResponse("登陆失败")

    login(request, user)
    return True

