
import json
import requests
import logging; logger = logging.getLogger(__name__)

from django.contrib.auth.models import User
from django.conf import settings



AppID = "wx0572e52dc3d9139a"
AppSecret = "a9ca60ddeba44a9117a762ed173ac2ef"

WX_TOKEN_URL = "https://api.weixin.qq.com/sns/oauth2/access_token?appid=%s&secret=%s&code=%s&grant_type=authorization_code"
UINFO_URL = "https://api.weixin.qq.com/sns/userinfo?access_token=%s&openid=%s"


class ZumbaBackend(object):

    # username  <-> openid
    # email     <-> headpic
    # last_name <-> nickName

    def authenticate(self, openId):
        logger.info("ZumbaBackend authenticate %s" % openId)

        try:
            user = User.objects.get(username=openId)
        except User.DoesNotExist:
            info = self.get_userinfo(openId)
            if not info:
                return
            user = User(username=openId, password='NULL',
                            email=info.get("headimgurl", ""),
                            last_name = info.get("nickname", ""))
            user.save()
        return user


    def get_user(self, uid):
        try:
            return User.objects.get(pk=uid)
        except User.DoesNotExist:
            return None


    def get_userinfo(self, openId):
        body = {
            "secret": settings.ZUMBA_SECRET,
            "method": "getUserInfo",
            "openId": openId
        }

        rep = requests.post(settings.UINFO_URL, json.dumps(body))
        if rep.ok:
            rep.encoding = "utf-8"
            info = rep.json()
            err = info.get("error_code")
            if err == 0:
                return info.get("user_info")
            else:
                logger.error("get userinfo err %s" % info)


