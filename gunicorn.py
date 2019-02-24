# -*- coding: utf-8 -*-
# @Author  : dmac

import os
import multiprocessing
bind = '0.0.0.0:80'      #绑定ip和端口号
backlog = 512                #监听队列
timeout = 30      #超时
worker_class = 'gevent' #使用gevent模式，还可以使用sync 模式，默认的是sync模式
workers = multiprocessing.cpu_count() * 2 + 1    #进程数
threads = 2 #指定每个进程开启的线程数
