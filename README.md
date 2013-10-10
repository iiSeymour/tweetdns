### tweetdns

A python service that tweets when your dynamic IP changes.

### dependencies

Python twitter API https://github.com/sixohsix/twitter

    $ easy_install twitter

### Steps

 - Create new twitter account for tweeting your IP
 - Make account private [optional]
 - Register account with https://dev.twitter.com/
 - Create new application to get a Consumer Key and Secret
 - Add Key and Secret to Tweeter class in tweetdns.py
 - Start daemon `./tweetdns start`
 - Follow your new twitter account to get updates when your IP changes
