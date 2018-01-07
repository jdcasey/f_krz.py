#!/usr/bin/env python

import yaml
import twitter
import json

AUTH_FILE = ".auth.yaml"

def score(f):
    score = 0
    if f.friends_count > 1000 and f.followers_count < 50:
        score = 5

    if f.statuses_count > 300:
        score = score + 5

    # score = (float(f.friends_count)/float(f.followers_count if f.followers_count > 0 else 1))
    # score = float(0 if f.protected is True else 1) * score
    # score = float(2 if f.followers_count < 30 else 1) * score
    # score = float(0.1 if f.statuses_count < 100 else 1) * score
    return score

with open(AUTH_FILE) as f:
    auth = yaml.load(f)

api = twitter.Api(consumer_key=auth['consumer_key'],
                      consumer_secret=auth['consumer_secret'],
                      access_token_key=auth['access_token'],
                      access_token_secret=auth['access_token_secret'], replay_dir='.replay')

followers = api.GetFollowers()
followers = [{
    'screen_name': f.screen_name, 
    'time_zone': f.time_zone, 
    'status_source': (f.status.source if f.status else "No Status Found"), 
    'statuses_count': f.statuses_count, 
    'followers': f.followers_count, 
    'friends': f.friends_count, 
    'score': score(f)
    } for f in followers]
followers = sorted(followers, key=lambda k: k['score']) 
#for f in (x for x in followers if x['score'] >= 10):
#   print f

by_sources = {}
for f in followers:
    if f['score'] < 8:
        continue

    src = f['status_source']
    if src is None:
        src = 'None'

    cubby = by_sources.get('src')
    if cubby is None:
        cubby = []
        by_sources[src] = cubby
    cubby.append(f)

for k in by_sources.keys():
    print k
    users = by_sources[k]
    for user in users:
        print "%(screen_name)s has score: %(score)s" % user