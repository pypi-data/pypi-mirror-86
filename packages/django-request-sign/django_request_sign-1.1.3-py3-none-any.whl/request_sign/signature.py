"""
@author: liyao
@contact: liyao2598330@126.com
@time: 2020/8/14 4:39 下午
"""
import re
import base64
import hashlib

from datetime import datetime

from django.core.cache import cache

from request_sign.utils import try_safe_eval
from request_sign.settings import SIGNATURE_METHOD, SIGNATURE_SECRET, SIGNATURE_ALLOW_TIME_ERROR, NONCE_CACHE_KEY, \
    SIGNATURE_PASS_URL, SIGNATURE_PASS_URL_NAME, SIGNATURE_PASS_URL_REGULAR

KEY_MAP = {
    'True': 'true',
    'False': 'false',
    'None': None
}

DELETE_KEY_MAP = ['[]', '{}', [], {}, None, '']


def signature_parameters(parameters):
    for p in parameters:
        if type(parameters[p]) == bytes:
            parameters[p] = str(parameters[p], encoding="utf-8")

    # 列表生成式，生成key=value格式
    parameters_list = ["".join(map(str, i)) for i in parameters.items() if i[1] and i[0] != "sign"]
    # 参数名ASCII码从小到大排序
    sort_parameters = "".join(sorted(parameters_list))
    # 在strA后面拼接上SIGNATURE_SECRET得到signature_str字符串
    signature_str = sort_parameters + SIGNATURE_SECRET
    # MD5加密
    m = hashlib.md5()
    m.update(signature_str.lower().encode('UTF-8'))
    return m.hexdigest()


def check_pass_url_regular(path):
    for r in SIGNATURE_PASS_URL_REGULAR:
        if re.search(r, path):
            return True

    return False


def is_number(str):
    try:
        if str == 'NaN':
            return False
        float(str)
        return True
    except:
        return False


def check_signature(request):
    # pass list
    if request.method.lower() not in SIGNATURE_METHOD or\
            request.path in SIGNATURE_PASS_URL or \
            request.path in SIGNATURE_PASS_URL_NAME or \
            check_pass_url_regular(request.path):
        return True

    timestamp = request.META.get("HTTP_TIMESTAMP")
    nonce = request.META.get("HTTP_NONCE")
    sign = request.META.get("HTTP_SIGN")

    # 判断cache是否正常
    if hasattr(cache, 'get') and hasattr(cache, 'set'):
        if cache.get(NONCE_CACHE_KEY.format(nonce=nonce)):
            return False
        else:
            cache.set(NONCE_CACHE_KEY.format(nonce=nonce), True, SIGNATURE_ALLOW_TIME_ERROR)

    if not all([timestamp, nonce, sign]):
        return False

    try:
        timestamp = float(timestamp)
    except:
        raise ValueError('timestamp must be int or float')

    now_timestamp = datetime.now().timestamp()
    if (now_timestamp - SIGNATURE_ALLOW_TIME_ERROR) > timestamp or timestamp > (
            now_timestamp + SIGNATURE_ALLOW_TIME_ERROR):
        return False

    parameters = {
        'nonce': base64.b64encode(bytes(str(nonce).lower(), encoding="utf8"))
    }
    get_parameters = request.GET.urlencode()
    post_parameters = request.POST.urlencode()
    body_parameters = str(request.body, encoding='utf-8')
    parameters = handle_parameter(parameters, get_parameters,
                                  post_parameters, body_parameters)
    return sign == signature_parameters(parameters)


def handle_parameter(parameters, get_parameters, post_parameters, body_parameters):
    parameter_list = []
    url_parameter_list = []
    for p in [get_parameters, post_parameters, body_parameters]:
        d = try_safe_eval(p)
        if isinstance(d, dict):
            parameter_list.append(d)
        elif isinstance(d, str):
            url_parameter_list.append(d)
    parameter_list.extend("&".join(url_parameter_list).split('&'))
    for parameter in parameter_list:
        if parameter:
            parameter = try_safe_eval(parameter)
            if isinstance(parameter, dict):
                # 遍历字典，对value进行url解码
                for p in parameter:
                    v = parameter[p]
                    if (v in DELETE_KEY_MAP or not v) and (not isinstance(v, (bool)) and not is_number(v)):
                        continue
                    v = re.sub(r"[^a-z\d]", "", str(parameter[p]).lower())
                    if not v or v in DELETE_KEY_MAP:
                        continue
                    parameters[p] = base64.b64encode(bytes(v, encoding="utf8"))

            else:
                if len(str(parameter).split('=')) == 2:
                    key, value = str(parameter).split('=')
                    if value not in DELETE_KEY_MAP:
                        # 解码并去除空格
                        value = re.sub(r"[^a-z\d]", "", str(value).lower())
                        parameters[key] = base64.b64encode(bytes(value, encoding="utf8"))
    return parameters
