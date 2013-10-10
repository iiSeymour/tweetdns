#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
import time
import urllib2
from daemon import Daemon


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


class TweetDNSDaemon(Daemon):

    def run(self):
        ip = ExternalIP()
        while True:
            time.sleep(5)
            if ip.newAddress():
                print "New IP %s" % ip.address


def main():
    daemon = TweetDNSDaemon('/tmp/tweetdns.pid')
    if len(sys.argv) > 1:
        if 'start' == sys.argv[1]:
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
