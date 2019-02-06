# -*- coding: utf-8 -*-
# @Author  : dmac

from flask import Blueprint

auth = Blueprint('auth', __name__)

from . import views
