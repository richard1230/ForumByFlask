#encoding: utf-8

from celery import Celery
# from app import create_app，有这句话就会有循环依赖的错误
from flask_mail import Message
from exts import mail
from flask import Flask
import config
from utils.CCPSDK import CCPRestSDK


# app = create_app(),
app = Flask(__name__)
app.config.from_object(config)
mail.init_app(app)
# alidayu.init_app(app)


# 运行本文件：
# 在windows操作系统上：
# celery -A tasks.celery worker --pool=solo --loglevel=info
# 在类*nix操作系统上：
# celery -A tasks.celery worker --loglevel=info

def make_celery(app):
    celery = Celery(app.import_name, backend=app.config['CELERY_RESULT_BACKEND'],
                    broker=app.config['CELERY_BROKER_URL'])
    celery.conf.update(app.config)
    TaskBase = celery.Task
    class ContextTask(TaskBase):
        abstract = True
        def __call__(self, *args, **kwargs):
            with app.app_context():
                return TaskBase.__call__(self, *args, **kwargs)
    celery.Task = ContextTask
    return celery

celery = make_celery(app)


@celery.task
def send_mail(subject,recipients,body):
    message = Message(subject=subject,recipients=recipients,body=body)
    mail.send(message)

# @celery.task
# def send_sms_captcha(telephone,captcha):
#     accountSid = "8a216da86f17653b016f3b4046b218ab"
#     accountToken = "ac156972012a43dab1782f1f89995ac9"
#     appId = "8a216da86f17653b016f3b40471818b2"
#     rest = CCPRestSDK.REST(accountSid, accountToken, appId)
#     rest.sendTemplateSMS(telephone, [captcha], "1")

