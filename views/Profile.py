# -*- coding: utf-8 -*-
from utils.commons import check_login
from BaseHandler import BaseHandler
from utils.response_code import RET
import constants
import logging
from utils.qiniu_storage import storage
class ProfileHandler(BaseHandler):
    @check_login
    def get(self):
        user_id=self.session.data['user_id']
        sql='select up_mobile,up_name,up_avatar from ih_user_profile where up_user_id=%s'
        try:
            ret=self.db.get(sql,user_id)
        except Exception as e:
            logging.error(e)
            return self.write(dict(errcode=RET.DBERR,errmsg='数据库查询错误'))
        if ret['up_avatar']:
            img_url=constants.QINIU_URL_PREFIX+ret['up_avatar']
        else:
            img_url=None
        self.write(dict(errcode=RET.OK,
                        errmsg='Ok',
                        data={"user_id":user_id,'name':ret['up_name'],'mobile':ret['up_mobile'],'avatar':img_url}))



class AvatarHandler(BaseHandler):
    @check_login
    def post(self):
        file=self.request.files
        img_files=file.get('avatar')
        if not img_files:
            return self.write(dict(errcode=RET.PARAMERR,errmsg='未传图片'))
        img_file=img_files[0]['body']
        try:
            key=storage(img_file)
        except Exception as e:
            logging.error(e)
            return self.write(dict(errcod=RET.THIRDERR,errmsg='上传失败'))
        user_id=self.session.data['user_id']
        sql= "update ih_user_profile set up_avatar=%(avatar)s where up_user_id=%(user_id)s"
        try:
            row_count=self.db.execute_rowcount(sql,avatar=key,user_id=user_id)
        except Exception as e:
            logging.error(e)
            return self.write(dict(errcod=RET.DBERR,errmsg='保存错误'))
        self.write(dict(errcode=RET.OK, errmsg="保存成功", data="%s%s" % (constants.QINIU_URL_PREFIX, key)))



class NameHandler(BaseHandler):
    @check_login
    def post(self, *args, **kwargs):
        name=self.json_args['name']
        user_id=self.session.data['user_id']
        if name in (None, ""):
            return self.write({"errcode": RET.PARAMERR, "errmsg": "params error"})
        sql= "update ih_user_profile set up_name=%(name)s where up_user_id=%(user_id)s"
        try:
            row_count=self.db.execute_rowcount(sql,name=name,user_id=user_id)
        except Exception as e:
            logging.error(e)
            return self.write(dict(errcod=RET.DBERR,errmsg='保存错误'))
        self.session.data["name"] = name
        try:
            self.session.save()
        except Exception as e:
            logging.error(e)
        self.write({"errcode": RET.OK, "errmsg": "OK"})
class AuthHandler(BaseHandler):
    """实名认证"""
    @check_login
    def get(self):
        # 在session中获取用户user_id
        user_id = self.session.data["user_id"]

        # 在数据库中查询信息
        try:
            ret = self.db.get("select up_real_name,up_id_card from ih_user_profile where up_user_id=%s", user_id)
        except Exception as e:
            # 数据库查询出错
            logging.error(e)
            return self.write({"errcode":RET.DBERR, "errmsg":"get data failed"})
        logging.debug(ret)
        if not ret:
            return self.write({"errcode":RET.NODATA, "errmsg":"no data"})
        self.write({"errcode":RET.OK, "errmsg":"OK", "data":{"real_name":ret.get("up_real_name", ""), "id_card":ret.get("up_id_card", "")}})

    @check_login
    def post(self):
        user_id = self.session.data["user_id"]
        real_name = self.json_args.get("real_name")
        id_card = self.json_args.get("id_card")
        if real_name in (None, "") or id_card in (None, ""):
            return self.write({"errcode":RET.PARAMERR, "errmsg":"params error"})
        # 判断身份证号格式
        try:
            self.db.execute_rowcount("update ih_user_profile set up_real_name=%s,up_id_card=%s where up_user_id=%s", real_name, id_card, user_id)
        except Exception as e:
            logging.error(e)
            return self.write({"errcode":RET.DBERR, "errmsg":"update failed"})
        self.write({"errcode":RET.OK, "errmsg":"OK"})