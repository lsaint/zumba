import requests
import time, random, string
import logging; logger = logging.getLogger(__name__)

import wechat_sdk
from django.conf import settings


def jsapi_ticket():
    body = {"secret": settings.ZUMBA_SECRET, "method": "getTicket"}
    rep = requests.post(settings.ZUMBA_API_URL, json=body)
    if not rep.ok:
        logger.error("get jsapi_ticket err")
        return ""
    info = rep.json()
    if str(info.get("error_code")) != "0":
        logger.error("get jsapi_ticket error_code %s" % info.get("error_code"))
        return ""
    return info.get("jsapi_ticket")


def wechat_ctx(request):
    context = {}
    context['appid'] = settings.ZUMBA_APPID
    context['timestamp'] = int(time.time())
    context['nonceStr'] = ''.join(random.sample(string.ascii_letters, 8))
    context['signature'] = WB.generate_jsapi_signature(
                        context['timestamp'],
                        context['nonceStr'],
                        request.build_absolute_uri(),
                        jsapi_ticket())
    return context


WB = wechat_sdk.basic.WechatBasic()

