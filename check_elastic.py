#!/usr/bin/python2

ELASTIC_HOST = 'localhost'
ELASTIC_INDEX = 'an_index'
ELASTIC_DATETIME = 'datetime'   # field storing datetime
ALLOWED_DELAY = 180         # Alert if the latest doc is older than this (sec)

MAIL_INTERVAL = 3600 * 24   # Re-send mail after this interval (seconds)
MAIL_SERVER = 'smtp.gmail.com:587'
MAIL_TO = 'your mail address'
MAIL_FROM = 'from mail address'
MAIL_USER = 'Google account'    # foobar@gmail.com etc.
MAIL_PASS = 'password (should be app password)'

DEBUG = False
DRYRUN = False


import datetime
import os
import pprint
import smtplib
import sys
from dateutil import parser
from elasticsearch import Elasticsearch

def get_filename(subject):
    return os.path.join('/var/tmp', subject + ".status")


def sendmail(subject, body):
    msg = 'Subject: %s\n\n%s' % (subject, body)

    if DRYRUN:
        print "Won't send email because of DRYRUN."
        return

    print "Sending mail alert..."

    server = smtplib.SMTP(MAIL_SERVER)
    server.starttls()
    server.login(MAIL_USER, MAIL_PASS)
    server.sendmail(MAIL_FROM, MAIL_TO, msg)

    print "Done."


def sendmail_if_required(subject, body='(none)'):
    filename = get_filename(subject)

    if os.path.isfile(filename):
        last_sent_time = os.stat(filename).st_mtime
    else:
        last_sent_time = 0.0

    passed_after_lastmail = \
            (datetime.datetime.utcnow() - datetime.datetime(1970,1,1)).\
                total_seconds() \
            - last_sent_time

    if passed_after_lastmail > MAIL_INTERVAL:
        sendmail(subject, body)
        open(filename, 'w').write('')


def cleanup(subject):
    filename = get_filename(subject)

    if os.path.isfile(filename):
        os.remove(filename)


def check():
    """
    Return True if need attention (the latest record is older than expect)
    """

    es = Elasticsearch([ELASTIC_HOST])
    res = es.search(index=ELASTIC_INDEX, body=\
            {
                # "query": {"match_all": {}},
                "from": 0,
                "size": 1,
                "sort": {
                    "datetime": {"order": "desc"}
                }
            })
    # pprint.pprint(res)
    last_doc_time = parser.parse(res['hits']['hits'][0]['_source']['datetime'])
    cur_time = datetime.datetime.utcnow()

    # print cur_time
    # print last_doc_time
    # print cur_time - last_doc_time
    delay = (cur_time - last_doc_time).total_seconds()

    if DEBUG:
        print delay

    if delay > ALLOWED_DELAY:
        return True
    else:
        return False


subject = "check_elastic"

ret = check()
if DEBUG:
    print ret

if ret:
    sendmail_if_required(subject, "Looks sps30 sensor is down")
else:
    cleanup(subject)
