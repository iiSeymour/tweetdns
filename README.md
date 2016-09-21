### TweetDNS

A python service that tweets when your dynamic IP changes.

### Setup

    $ virtualenv -p python3 venv
    $ source venv/bin/activate
    $ python -m pip install -r requirements.txt
    $ ./tweetdns start

### Steps

 - Register your twitter account with https://dev.twitter.com/
 - Create new application to get a Consumer Key and Secret
 - Set the permissions to `Read, Write and Access direct messages`
 - Add user, key and secret in `settings.py`
 - Start daemon `./tweetdns start`
 - Recieve direct messages to your user account when your IP address changes
