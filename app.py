#!/usr/bin/env python3
# coding:utf-8

import threading
#from flask import Flask
from gevent.pywsgi import WSGIServer
from nemo.web.flask_app import web_app
from instance import config


'''
系统入口，启动web server
'''


#flask_app = Flask(__name__)
ProductionConfig = config.ProductionConfig
#flask_app.config.from_object(ProductionConfig)
host = ProductionConfig.WEB_HOST#flask_app.config.get('WEB_HOST')
port = ProductionConfig.WEB_PORT#flask_app.config.get('WEB_PORT')
thread_pool = []


def web_server():
    http_server = WSGIServer((host, port), web_app)
    http_server.serve_forever()


def main():
    print("* Running on http://" + host + ":" + str(port))
    thread_pool.append(threading.Thread(target=web_server, args=()))
    try:
        for t in thread_pool:
            t.start()
        for t in thread_pool:
            t.join()
    except Exception as e:
        print(e)


if __name__ == '__main__':
    main()
    # pass
