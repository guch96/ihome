# -*- coding: utf-8 -*-
import BaseHandler
import re
import logging
import hashlib
import config
from utils.response_code import *
from utils.session import Session
from utils.commons import check_login
class RegisterHandler(BaseHandler.BaseHandler):
    def post(self):
        # 获取参数
        mobile = self.json_args.get("mobile")
        sms_code = self.json_args.get("phonecode")
        password = self.json_args.get("password")
        if not all([mobile, sms_code, password]):
            return self.write(dict(errcode=RET.PARAMERR, errmsg="参数不完整"))

        if not re.match(r"^1\d{10}$", mobile):
            return self.write(dict(errcode=RET.DATAERR, errmsg="手机号格式错误"))
        try:
            real_sms_code=self.redis.get('sms_code_%s'%mobile)
        except Exception as e:
            logging.error(e)
            return self.write(dict(errcode=RET.DBERR, errmsg="查询错误"))
        if not real_sms_code:
            return self.write(dict(errcode=RET.NODATA, errmsg="验证码过期"))
        # 对比用户填写的验证码与真实值
        # if real_sms_code != sms_code and  sms_code != "2468":
        if real_sms_code != str(sms_code):
            return self.write(dict(errcode=RET.DATAERR, errmsg="验证码错误"))
        #删除短信验证码
        try:
            self.redis.delete("sms_code_%s" % mobile)
        except Exception as e:
            logging.error(e)
        #注册帐号
        passwd = hashlib.sha256(password + config.passwd_hash_key).hexdigest()
        sql = "insert into ih_user_profile(up_name, up_mobile, up_passwd) values(%(name)s, %(mobile)s, %(passwd)s);"
        try:
            user_id = self.db.execute(sql, name=mobile, mobile=mobile, passwd=passwd)
        except Exception as e:
            logging.error(e)
            return self.write(dict(errcode=RET.DATAEXIST, errmsg="手机号已存在"))

        try:
            self.session=Session(self)
            self.session.data['user_id']=user_id
            self.session.data['mobile']=mobile
            self.session.data['name']=mobile
            self.session.save()
        except Exception  as e:
            logging.error(e)
        self.write(dict(errcode=RET.OK, errmsg="注册成功"))
class LoginHandler(BaseHandler.BaseHandler):

    def post(self):
        mobile = self.json_args.get("mobile")
        password = self.json_args.get("password")
        if not all([mobile,password]):
            return self.write(dict(errcode=RET.PARAMERR, errmsg="参数不完整"))
        if not re.match(r"^1\d{10}$", mobile):
            return self.write(dict(errcode=RET.DATAERR, errmsg="手机号格式错误"))
        passwd = hashlib.sha256(password + config.passwd_hash_key).hexdigest()
        res = self.db.get("select up_user_id,up_name,up_passwd from ih_user_profile where up_mobile=%(mobile)s",
                          mobile=mobile)
        password = hashlib.sha256(password + config.passwd_hash_key).hexdigest()
        print type(password)
        print password
        print type(res['up_passwd'])
        print res['up_passwd']
        if res and res["up_passwd"] == unicode(password):
            # 生成session数据
            # 返回客户端
            try:
                self.session = Session(self)
                self.session.data['user_id'] = res['up_user_id']
                self.session.data['name'] = res['up_name']
                self.session.data['mobile'] = mobile
                self.session.save()
            except Exception as e:
                logging.error(e)
            return self.write(dict(errcode=RET.OK, errmsg="OK"))
        else:
            return self.write(dict(errcode=RET.DATAERR, errmsg="手机号或密码错误！"))

class LogoutHandler(BaseHandler.BaseHandler):
    """退出登录"""
    @check_login
    def get(self):
        # 清除session数据
        # sesssion = Session(self)
        self.session.clear()
        self.write(dict(errcode=RET.OK, errmsg="退出成功"))


class CheckLoginHandler(BaseHandler.BaseHandler):
    def get(self):
        if self.get_current_user():
            self.write({"errcode": RET.OK, "errmsg": "true", "data": {"name": self.session.data.get("name")}})
        else:
            self.write({"errcode": RET.SESSIONERR, "errmsg": "false"})

