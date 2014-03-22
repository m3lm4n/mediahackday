from django.db import models
from django.db.models.base import Model
from django.db.models.fields import CharField
from utils import ModelMixins
from django.conf import settings
from apnsclient import Session, APNs, Message

class APNTokenModel(Model, ModelMixins):
    token = CharField(primary_key=True, max_length=255)

    @staticmethod
    def send_notification(title):
        tokens = APNTokenModel.objects.all()
        print 'APN tokens found: %s' % len(tokens)
        tokens_list = []
        for token in tokens:
            tokens_list.append(token.token)

        con = Session.new_connection("push_sandbox", cert_file=settings.APN_PERM)
        # New message to 3 devices. You app will show badge 10 over app's icon.
        print "Sending notification for tokens %s" % tokens_list

        # weird names because we dont have a lot of space to send messages to APN
        payload = {
            'aps': {
                'alert': '`%s` added' % title
            }
        }
        message = Message(tokens_list, payload=payload)

        # Send the message.
        srv = APNs(con)
        res = srv.send(message)

        # Check failures. Check codes in APNs reference docs.
        for token, reason in res.failed.items():
            code, errmsg = reason
            print "APN: Device faled: %s, reason: %s" % (token, errmsg)

        # Check failures not related to devices.
        for code, errmsg in res.errors:
            print "APN: Error in APN: %s" % errmsg

        # Check if there are tokens that can be retried
        if res.needs_retry():
            # repeat with retry_message or reschedule your task
            retry_message = res.retry()
            print "APN: Retry message: %s" % retry_message

