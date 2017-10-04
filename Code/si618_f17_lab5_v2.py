#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Oct  3 23:57:23 2017

@author: ruixin
"""

import urllib3
import json


access_token = ##YOUR ACCESS CODE

page_id = "nytimes"

# construct the URL string
base = "https://graph.facebook.com/v2.10"
node = "/" + page_id + "/posts"
parameters = "/?fields=created_time,id&since=2017-09-20&until=2017-09-26&access_token=%s" % access_token
url = base + node + parameters

http = urllib3.PoolManager()
r = http.request('GET', url)

data = json.loads(r.data)

has_next_page = True
posts_in_date = []
posts_in_date.append(data)
while(has_next_page):
    if 'paging' in data.keys():
        try:
            r = http.request('GET', data['paging']['next'])
            data = json.loads(r.data)
            posts_in_date.append(data)
        except:
            has_next_page = False
    else:
        has_next_page = False
post_id = []
for post in posts_in_date:
    for j in post['data']:
       post_id.append(j['id'])

# Now time to start to look at the comments.
parameters_c = "/?filter=stream&fields=id,message&access_token=%s" % access_token
comments = []
for i in post_id:
    next_page_c = True
    node_c = "/" + i + "/comments"
    url_c = base + node_c + parameters_c
    u = http.request('GET', url_c)
    com = json.loads(u.data)
    comments.append(com['data'])
    while(next_page_c):
        if 'paging' in com.keys():
            try:
                r1 = http.request('GET', com['paging']['next'])
                com = json.loads(r1.data)
                comments.append(com['data'])
            except KeyError:
                next_page_c = False
        else:
            next_page_c = False

d = {}
for item in comments:
    for c in item:
        d[c['id']] = c['message']
