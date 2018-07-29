# -*- coding: utf-8 -*-
import tornado.web
import tornado.httpclient
import tornado.gen
from libs.SDK import SendTemplateSMS
import datetime
import md5
import base64
import datetime
import urllib2
import json
from xmltojson import xmltojson
from xml.dom import minidom
class demo(tornado.web.RequestHandler):
    def __int__(self):
        # 请求地址，格式如下，不需要写http://
        self.ServerIP = 'app.cloopen.com';
        # 请求端口
        self.ServerPort = '8883';
        self.AccountSid='8aaf070864a7ad6d0164ad3f3ddc0552'
        self.AccountToken='9c8828ef035b4821a282fe26a03c2e45'
        self.AppId='8aaf070864a7ad6d0164ad3f3e330558'
        self.SoftVersio='2013-12-26'
        self.Batch=''

        # REST版本号
    @tornado.gen.coroutine
    def post(self, *args, **kwargs):
        self.BodyType = 'json'
        moblie=self.get_argument('moblie')
        content=self.get_argument('content')
        datas=[content,5]
        # t=SendTemplateSMS(moblie, [content, 5], 1)
        # res=tornado.httpclient.AsyncHTTPClient()
        # yield res.fetch()
    # def sendTemplateSMS(self, to, datas, tempId):
        # self.accAuth()
        nowdate = datetime.datetime.now()
        self.Batch = nowdate.strftime("%Y%m%d%H%M%S")
        # 生成sig
        signature = '8aaf070864a7ad6d0164ad3f3ddc0552' + '9c8828ef035b4821a282fe26a03c2e45'+ self.Batch;
        sig = md5.new(signature).hexdigest().upper()
        # 拼接URL
        url = "https://" + 'app.cloopen.com' + ":" + '8883' + "/" + '2013-12-26' + "/Accounts/" + '8aaf070864a7ad6d0164ad3f3ddc0552' + "/SMS/TemplateSMS?sig=" + sig
        # 生成auth
        src = '8aaf070864a7ad6d0164ad3f3ddc0552' + ":" + self.Batch;
        auth = base64.encodestring(src).strip()
        # req = urllib2.Request(url)
        # self.setHttpHeader(req)
        # req.add_header("Authorization", auth)
        # 创建包体
        b = ''
        for a in datas:
            b += '<data>%s</data>' % (a)

        body = '<?xml version="1.0" encoding="utf-8"?><SubAccount><datas>' + b + '</datas><to>%s</to><templateId>%s</templateId><appId>%s</appId>\
            </SubAccount>\
            ' % (moblie, 1, '8aaf070864a7ad6d0164ad3f3e330558')
        if self.BodyType == 'json':
            # if this model is Json ..then do next code
            b = '['
            for a in datas:
                b += '"%s",' % (a)
            b += ']'
            body = '''{"to": "%s", "datas": %s, "templateId": "%s", "appId": "%s"}''' % (moblie, b, 1, '8aaf070864a7ad6d0164ad3f3e330558')
        # req.add_data(body)
        headers={}
        if self.BodyType == 'json':
            # req.add_header("Accept", "application/json")
            # req.add_header("Content-Type", "application/json;charset=utf-8")
             headers={"Accept": "application/json",
                      "Content-Type":"application/json;charset=utf-8",
                      "Authorization": auth}
        else:
            # req.add_header("Accept", "application/xml")
            # req.add_header("Content-Type", "application/xml;charset=utf-8")
            headers = {"Accept": "application/xml",
                       "Content-Type": "application/xml;charset=utf-8",
                       "Authorization": auth}
        data = ''
        try:
            # res = urllib2.urlopen(req);
            # data = res.read()
            # res.close()
            #
            # if self.BodyType == 'json':
            #     # json格式
            #     locations = json.loads(data)
            # else:
            #     # xml格式
            #     xtj = xmltojson()
            #     locations = xtj.main(data)
            # if self.Iflog:
            #     self.log(url, body, data)
            # return locations
            http_client = tornado.httpclient.AsyncHTTPClient()
            resp = yield tornado.gen.Task(
                http_client.fetch,
                url,
                method="POST",
                headers=headers,
                body=body,
                validate_cert=False)
            print resp.body

        except Exception as error:
            # if self.Iflog:
            #     self.log(url, body, data)
            # return { '172001': '网络错误'}
            print error

