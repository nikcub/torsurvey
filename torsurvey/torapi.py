#!/usr/bin/env python
"""
  cexbot.cexapi
"""

import requesocks as requests
import requesocks.exceptions
# import hmac
# import hashlib
# import json
import logging
# from time import time

class TorAPI(object):

  headers = {
    'User-Agent' : 'torsurvey-',
    }

  tor_host = None
  tor_port = None

  proxy_tor = {
    "http": "socks5://127.0.0.1:9030",
    "https": "socks5://127.0.0.1:9030"
  }

  def __init__(self, proxy_host='127.0.0.1', proxy_port='9040', proxy_type='socks5'):
    self.proxy_host = proxy_host
    self.proxy_port = proxy_port
    self.proxy_type = proxy_type
    self.proxy = {}
    self.proxy['http'] = "%s://%s:%d" % (proxy_type, proxy_host, int(proxy_port))
    self.proxy['https'] = "%s://%s:%d" % (proxy_type, proxy_host, int(proxy_port))
    self.session = requesocks.session()
    self.session.proxies = self.proxy
    logging.debug("Established session with proxies %s" % str(self.proxy))

  def get_ip(self):
    r = self.req('http://ifconfig.me/ip')
    if r.status_code == 200:
      return r.text
    return 'Error'

  def get_headers(self):
    headers = self.headers
    # @TODO add headers
    return headers

  def req(self, url, extras={}):
    try:
      r = self.session.request('GET', url, allow_redirects=True, headers=self.headers)
    except requesocks.exceptions.ConnectionError, e:
      logging.error("Bad connection cannot connect to %s" % url)
      return False
    # if r.headers['Content-Type'] != 'text/json' or not r.text:
    #   logging.error("Request error (%s)" % r.text[:200])
    #   return False
    # print r
    return r
