#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import sys
import time
from urllib.request import urlopen

from twitter import oauth_dance, read_token_file, OAuth, Twitter

import settings
from daemon import Daemon


def get_address():
    """
    Get external IP address
    """
    return urlopen(settings.site).read()


class Tweeter(object):

    def __init__(self):

        USER = settings.user
        CONSUMER_KEY = settings.consumer_key
        CONSUMER_SECRET = settings.consumer_secret

        if not (USER and CONSUMER_KEY and CONSUMER_SECRET):
            print("Whoa! Fill in your details in settings.py first!")
            sys.exit(1)

        TWITTER_CREDS = os.path.expanduser('~/.tweetdns')

        if not os.path.exists(TWITTER_CREDS):
            oauth_dance(sys.argv[0], CONSUMER_KEY, CONSUMER_SECRET, TWITTER_CREDS)

        oauth_token, oauth_secret = read_token_file(TWITTER_CREDS)
        self.twitter = Twitter(auth=OAuth(oauth_token, oauth_secret, CONSUMER_KEY, CONSUMER_SECRET))

    def tweet(self, ip):
        """
        Tweet new IP address
        """
        self.twitter.statuses.update(status=ip)

    def direct_message(self, text):
        self.twitter.direct_messages.new(user=settings.user, text=text)


class TweetDNSDaemon(Daemon):

    def nest(self, tweeter):
        """
        Initialise a tweeter before daemonizing
        """
        self.tweeter = tweeter()

    def run(self):

        ip = get_address()

        while True:
            new_ip = get_address()
            if ip == new_ip:
                print("IP is still %s" % ip.decode())
            else:
                ip = new_ip
                text = "New IP %s" % ip.decode()
                print(text)
                self.tweeter.direct_message(text=text)

            time.sleep(settings.seconds)


def main():

    daemon = TweetDNSDaemon('/tmp/tweetdns.pid')

    if len(sys.argv) > 1:
        if 'start' == sys.argv[1]:
            daemon.nest(Tweeter)
            daemon.start()
        elif 'stop' == sys.argv[1]:
            daemon.stop()
        elif 'restart' == sys.argv[1]:
            daemon.restart()
        elif 'status' == sys.argv[1]:
            if daemon.status:
                print("* %s is running: %s" % (sys.argv[0], daemon.pid))
            else:
                print("* %s is not running" % sys.argv[0])
        else:
            print("Unknown command")
            sys.exit(2)
        sys.exit(0)
    else:
        print("usage: %s start|stop|restart|status" % sys.argv[0])
        sys.exit(2)

if __name__ == "__main__":
    main()
