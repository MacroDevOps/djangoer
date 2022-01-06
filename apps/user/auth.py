import hashlib

import ldap3
from django.contrib.auth import get_user_model
from django.contrib.auth.backends import ModelBackend, UserModel
from rest_framework.permissions import BasePermission

from fuservice.settings import LDAP_URL

User = get_user_model()


def ldap_auth(username, password):
    try:
        username = 'tkoffice\\%s' % username
        server = ldap3.Server(LDAP_URL)
        conn = ldap3.Connection(server, user=username, password=password, authentication=ldap3.NTLM)
        return conn.bind()
    except Exception as e:
        print(e)


def hash_password(password):
    if isinstance(password, str):
        password = password.encode('utf-8')
    return hashlib.md5(password).hexdigest().upper()


def ldap_auth_add_user(username, password):
    if ldap_auth(username, password):
        if not UserModel.objects.filter(username=username).exists():
            addUser = UserModel()
            addUser.username = username
            addUser.set_password(password)
            addUser.save()
        return True


class CumstomBackend(ModelBackend):
    def authenticate(self, request, username=None, password=None, **kwargs):
        # if ldap_auth_add_user(username, password): TODO 测试环境中登录暂时不需要进行验证。
        if True:
            return UserModel._default_manager.get_by_natural_key(username)


def jwt_response_payload_handler(token, user=None, request=None):
    return {
        'status': 200,
        'token': token,
    }


# TODO 钉钉第三方介入 https://www.cnblogs.com/tjw-bk/p/14164513.html
class OrganizerPermission(BasePermission):
    message = "必须是organizer才能访问"

    def has_permission(self, request, view):
        if request.user.user_type != 3:
            return False
        return True
