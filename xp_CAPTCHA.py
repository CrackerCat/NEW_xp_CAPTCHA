#!/usr/bin/env python
#coding:gbk
from burp import IBurpExtender
from burp import IIntruderPayloadGeneratorFactory
from burp import IIntruderPayloadGenerator
import base64
import json
import re
import urllib2
import ssl

host = ('127.0.0.1', 8899)

class BurpExtender(IBurpExtender, IIntruderPayloadGeneratorFactory):
    def registerExtenderCallbacks(self, callbacks):
        #ע��payload������
        callbacks.registerIntruderPayloadGeneratorFactory(self)
        #���������ʾ������
        callbacks.setExtensionName("xp_CAPTCHA")
        print 'xp_CAPTCHA  ������:Ϲ����֤��\nblog��http://www.nmd5.com/\nT00ls��https://www.t00ls.net/ \nThe loner��ȫ�Ŷ� author:�����[��\n\n�÷���\n��headͷ�����xiapao:��֤���URL\n\n�磺\n\nPOST /login HTTP/1.1\nHost: www.baidu.com\nUser-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:84.0) Gecko/20100101 Firefox/84.0\nAccept: text/plain, */*; q=0.01\nAccept-Language: zh-CN,zh;q=0.8,zh-TW;q=0.7,zh-HK;q=0.5,en-US;q=0.3,en;q=0.2\nContent-Type: application/x-www-form-urlencoded; charset=UTF-8\nX-Requested-With: XMLHttpRequest\nxiapao:http://www.baidu.com/get-validate-code\nContent-Length: 84\nConnection: close\nCookie: JSESSIONID=24D59677C5EDF0ED7AFAB8566DC366F0\n\nusername=admin&password=admin&vcode=8888\n\n'

    def getGeneratorName(self):
        return "xp_CAPTCHA"

    def createNewInstance(self, attack):
        return xp_CAPTCHA(attack)

class xp_CAPTCHA(IIntruderPayloadGenerator):
    def __init__(self, attack):
        tem = "".join(chr(abs(x)) for x in attack.getRequestTemplate()) #request����
        cookie = re.findall("Cookie: (.+?)\r\n", tem)[0] #��ȡcookie
        xp_CAPTCHA = re.findall("xiapao:(.+?)\r\n", tem)[0]
        ssl._create_default_https_context = ssl._create_unverified_context #����֤�飬��ֹ֤�鱨��
        print xp_CAPTCHA+'\n'
        print 'cookie:' + cookie+'\n'
        self.xp_CAPTCHA = xp_CAPTCHA
        self.cookie = cookie
        self.max = 1 #payload���ʹ�ô���
        self.num = 0 #���payload��ʹ�ô���
        self.attack = attack

    def hasMorePayloads(self):
        #���payloadʹ�õ���������reset����0
        if self.num == self.max:
            return False  # ���ﵽ��������ʱ��͵���reset
        else:
            return True

    def getNextPayload(self, payload):  # ��������뿴���Ľ���
        xp_CAPTCHA_url = self.xp_CAPTCHA #��֤��url

        print xp_CAPTCHA_url
        headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.103 Safari/537.36","Cookie":self.cookie}
        request = urllib2.Request(xp_CAPTCHA_url,headers=headers)
        CAPTCHA = urllib2.urlopen(request) #��ȡͼƬ
        CAPTCHA_base64 = base64.b64encode(CAPTCHA.read()) #��ͼƬbase64����

        request = urllib2.Request('http://%s:%s/base64'%host, 'base64='+CAPTCHA_base64)
        response = urllib2.urlopen(request).read()
        print(response)
        return response

    def reset(self):
        self.num = 0  # ����
        return