#coding=gbk

#coding=utf-8

#-*- coding: UTF-8 -*-  

from CCPRestSDK import REST
import ConfigParser
import tornado.gen

#���ʺ�
accountSid= '8aaf070864a7ad6d0164ad3f3ddc0552';

#���ʺ�Token
accountToken= '9c8828ef035b4821a282fe26a03c2e45';

#Ӧ��Id
appId='8aaf070864a7ad6d0164ad3f3e330558';

#�����ַ����ʽ���£�����Ҫдhttp://
serverIP='app.cloopen.com';

#����˿� 
serverPort='8883';

#REST�汾��
softVersion='2013-12-26';

  # ����ģ�����
  # @param to �ֻ�����
  # @param datas �������� ��ʽΪ���� ���磺{'12','34'}���粻���滻���� ''
  # @param $tempId ģ��Id
# # class
# def sendTemplateSMS(to,datas,tempId):
#
#
#     #��ʼ��REST SDK
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
# #sendTemplateSMS(�ֻ�����,��������,ģ��Id)
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
    ccp.sendTemplateSMS("13023208560", ["���������", 5], 1)
