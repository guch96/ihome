#coding=gbk

#coding=utf-8

#-*- coding: UTF-8 -*-  

from CCPRestSDK import REST
import ConfigParser
import tornado.gen

#主帐号
accountSid= '8aaf070864a7ad6d0164ad3f3ddc0552';

#主帐号Token
accountToken= '9c8828ef035b4821a282fe26a03c2e45';

#应用Id
appId='8aaf070864a7ad6d0164ad3f3e330558';

#请求地址，格式如下，不需要写http://
serverIP='app.cloopen.com';

#请求端口 
serverPort='8883';

#REST版本号
softVersion='2013-12-26';

  # 发送模板短信
  # @param to 手机号码
  # @param datas 内容数据 格式为数组 例如：{'12','34'}，如不需替换请填 ''
  # @param $tempId 模板Id
# # class
# def sendTemplateSMS(to,datas,tempId):
#
#
#     #初始化REST SDK
#     rest = REST(serverIP,serverPort,softVersion)
#     rest.setAccount(accountSid,accountToken)
#     rest.setAppId(appId)
#
#     result = rest.sendTemplateSMS(to,datas,tempId)
#     for k,v in result.iteritems():
#
#         if k=='templateSMS' :
#                 for k,s in v.iteritems():
#                     print '%s:%s' % (k, s)
#         else:
#             print '%s:%s' % (k, v)
#
#
# #sendTemplateSMS(手机号码,内容数据,模板Id)
class CCP(object):

    def __init__(self):
        self.rest = REST(serverIP, serverPort, softVersion)
        self.rest.setAccount(accountSid, accountToken)
        self.rest.setAppId(appId)

    @staticmethod
    def instance():
        if not hasattr(CCP, "_instance"):
            CCP._instance = CCP()
        return CCP._instance
    @tornado.gen.coroutine
    def sendTemplateSMS(self, to, datas, tempId):
        try:
            result =yield self.rest.sendTemplateSMS(to, datas, tempId)
            print 'ccccc'
            print result
        except Exception as e:
            print e
            print 'ascf'
        if result.get("statusCode") == "000000":
            raise tornado.gen.Return(1)
        else:
            raise tornado.gen.Return(0)

ccp = CCP.instance()

if __name__ == "__main__":
    ccp = CCP.instance()
    ccp.sendTemplateSMS("13023208560", ["我是你儿子", 5], 1)
