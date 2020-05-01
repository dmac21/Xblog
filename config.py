# -*- coding: utf-8 -*-
# @Author  : dmac

import os
import datetime

basedir = os.path.abspath(os.path.dirname(__file__))


class Config(object):
    SECRET_KEY = 'hard to guess string'
    DEBUG = True
    MAIL_SERVER = 'smtp.qq.com'
    MAIL_PORT = 465
    MAIL_USE_SSL = True
    MAIL_USERNAME = '1073838586@qq.com'
    MAIL_PASSWORD = 'wkanmnnbqrzchjgb'
    SQLALCHEMY_DATABASE_URI = 'mysql://root:F825c9e08b@@127.0.0.1/xblog?charset=utf8'
    SEND_FILE_MAX_AGE_DEFAULT = datetime.timedelta(seconds=1)
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    XBLOG_MAIL_SUBJECT_PREFIX = '[Xblog]'
    XBLOG_MAIL_SENDER = 'Xblog Admin <1073838586@qq.com>'
    XBLOG_ADMIN = '1073838586@qq.com'
    QINIU_AK = 'LrU-HGHiDtPz7-yp7cGJ8fGIom1dThcxCwi-1YOP'
    QINIU_SK = 'GjvnMyzgL-dUXFba0L2zU_yjXE1Be39c3eLC6RoT'
    QINIU_BUCKET = 'xblog'
    QINIU_DOMAIN = 'http://pn6gtjkb6.bkt.clouddn.com'

    @staticmethod
    def init_app(app):
        pass


config = Config()
