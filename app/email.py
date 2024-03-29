import os
from flask import render_template, current_app, url_for
from threading import Thread
from flask_mail import Message
from app import mail

basedir = os.path.abspath(os.path.dirname(__file__))


class EmailSender:
    def send_async_mail(self, app, msg, **kwargs):
        print('开始异步发送')
        with app.app_context():
            mail.send(msg)
        print('发送成功')

    def send_mail(self, to, subject, template, **kwargs):
        msg = Message(current_app.config['STFU_MAIL_SUBJECT_PREFIX'] + subject,
                      sender=current_app.config['MAIL_SENDER'], recipients=[to])
        msg.body = render_template(template + '.txt', **kwargs)
        msg.html = render_template(template + '.html', **kwargs)
        thr = Thread(target=self.send_async_mail, args=[current_app._get_current_object(), msg])
        thr.start()
        return thr

    def send_picture_mail(self, to, subject, template, **kwargs):
        application = current_app._get_current_object()
        msg = Message(current_app.config['STFU_MAIL_SUBJECT_PREFIX'] + subject,
                      sender=current_app.config['MAIL_SENDER'], recipients=[to])


        msg.body = render_template(template + '.txt', **kwargs)
        # msg.html = render_template(template + '.html', img_1='cid:bg_1.jpg', img_2='cid:work-1.jpg',
        #                            img_3='cid:work-2.jpg', **kwargs)
        msg.html = render_template(template + '.html', **kwargs)

        thr = Thread(target=self.send_async_mail, args=[application, msg])
        thr.start()
        return thr
