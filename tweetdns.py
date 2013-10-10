#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import sys
import time
import urllib2
from daemon import Daemon
from twitter import oauth_dance, read_token_file, OAuth, Twitter


class ExternalIP(object):

    def __init__(self):
        self.address = None
        self.address_site = "http://canihazip.com/s"

    def getAddress(self):
        '''
        Get external IP address
        '''
        return urllib2.urlopen(self.address_site).read()

    def newAddress(self):
        '''
        Check if the IP address has changed
        '''
        ip = self.getAddress()
        if ip != self.address:
            self.address = ip
            return True
        return False


class Tweeter(object):

    def __init__(self):

        CONSUMER_KEY = None
        CONSUMER_SECRET = None

        if not (CONSUMER_KEY and CONSUMER_SECRET):
            raise Exception("Whoa! Fill in your keys first!")

        TWITTER_CREDS = os.path.expanduser('~/.tweetdns')

        if not os.path.exists(TWITTER_CREDS):
            oauth_dance("tweetdns", CONSUMER_KEY, CONSUMER_SECRET, TWITTER_CREDS)

        oauth_token, oauth_secret = read_token_file(TWITTER_CREDS)
        tauth = OAuth(oauth_token, oauth_secret, CONSUMER_KEY, CONSUMER_SECRET)
        self.twitter = Twitter(auth=tauth)

    def tweet(self, ip):
        '''
        Tweet new IP address
        '''
        self.twitter.statuses.update(status=ip)


class TweetDNSDaemon(Daemon):

    def nest(self, tweeter):
        '''
        Initialise a tweeter before daemonizing
        '''
        self.tweet = tweeter()

    def run(self):
        ip = ExternalIP()
        while True:
            if ip.newAddress():
                self.tweet.tweet("New IP %s" % ip.address)
            time.sleep(3600)


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
        else:
            print "Unknown command"
            sys.exit(2)
        sys.exit(0)
    else:
        print "usage: %s start|stop|restart" % sys.argv[0]
        sys.exit(2)

if __name__ == "__main__":
    main()
