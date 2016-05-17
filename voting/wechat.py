import requests
import time, random, string
import logging; logger = logging.getLogger(__name__)

import wechat_sdk
from django.conf import settings


class WechatBasicEx(wechat_sdk.basic.WechatBasic):


    def __init__(self, token=None, appid=None, appsecret=None, partnerid=None,
                 partnerkey=None, paysignkey=None, access_token=None, access_token_expires_at=None,
                 jsapi_ticket=None, jsapi_ticket_expires_at=None, checkssl=False):

        wechat_sdk.basic.WechatBasic.__init__(self, token=token, appid=appid, appsecret=appsecret,
                partnerid=partnerid, partnerkey=partnerkey, paysignkey=paysignkey,
                access_token=access_token, access_token_expires_at=access_token_expires_at,
                jsapi_ticket=jsapi_ticket, jsapi_ticket_expires_at=jsapi_ticket_expires_at,
                checkssl=checkssl)


    @property
    def access_token(self):
        url = "http://wxuat.watsonsestore.com.cn/clickWap/rest/wx/proxy"
        body = {"secret": settings.ZUMBA_SECRET, "method": "getToken"}
        rep = requests.post(url, json=body)
        if not rep.ok:
            logger.error("get access_token err")
            return ""
        info = rep.json()
        if str(info.get("error_code")) != "0":
            logger.error("get access_token error_code %s" % info.get("error_code"))
            return ""
        return info.get("access_token")



def wechat_ctx(request):
    context = {}
    context['appid'] = settings.ZUMBA_APPID
    context['timestamp'] = int(time.time())
    context['nonceStr'] = ''.join(random.sample(string.ascii_letters, 8))
    context['signature'] = WB.generate_jsapi_signature(
                        context['timestamp'],
                        context['nonceStr'],
                        request.build_absolute_uri())
    return context


WB = WechatBasicEx(appid=settings.ZUMBA_APPID, appsecret=settings.ZUMBA_SECRET)

