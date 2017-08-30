from django.shortcuts import render
import hashlib

from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from lxml import etree
from django.utils.encoding import smart_str
import time
from utils import xmltodict

# Create your views here.

def hello(request):
    return HttpResponse('Hello')
@csrf_exempt
def check(request):
    """
    所有的消息都会先进入这个函数进行处理，函数包含两个功能，
    微信接入验证是GET方法，
    微信正常的收发消息是用POST方法。
    """
    if request.method == "GET":
        signature = request.GET.get("signature", None)
        timestamp = request.GET.get("timestamp", None)
        nonce = request.GET.get("nonce", None)
        echostr = request.GET.get("echostr", None)
        token = 'success'
        tmp_list = [token, timestamp, nonce]
        tmp_list.sort()
        tmp_str = "%s%s%s" % tuple(tmp_list)
        tmp_str = tmp_str.encode('UTF-8')
        tmp_str = hashlib.sha1(tmp_str).hexdigest()
        if tmp_str == signature:
            return HttpResponse(echostr)
        else:
            return HttpResponse("failed")
    elif request.method == 'POST':
        xml_str = smart_str(request.body)
        request_xml = etree.fromstring(xml_str)
        response_xml = xmltodict.convertxml(request_xml)  # 修改这
        return HttpResponse(etree.tostring(response_xml))
