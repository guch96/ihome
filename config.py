# -*- coding: utf-8 -*-
import os
BASH_PATH=os.path.dirname(__file__)
settings={
    'debug':True,
    'static_path': os.path.join(BASH_PATH, 'static'),
    'cookie_secret':'HcW5tyJuRKWiVsQoXZNOB/cMyp24NkA5r+8Sw6tCCao=',
    'xsrf_cookies' :True,
    'login_url':'/login'
}

mysql_options = dict(
    host="127.0.0.1",
    database="ihome",
    user="root",
    password="1234"
)

redis_options = dict(
    host="127.0.0.1",
    port="6379"
)
log_path=os.path.join(BASH_PATH,'logs/log')
log_level='debug'

passwd_hash_key = "nlgCjaTXQX2jpupQFQLoQo5N4OkEmkeHsHD9+BBx2WQ="