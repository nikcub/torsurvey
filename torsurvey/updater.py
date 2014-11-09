#!/usr/bin/env python
"""
  torsurvey.updater
"""

import requesocks
import torsurvey
import logging

UPDATE_URL = "https://raw.github.com/nikcub/torsurvey/master/VERSION"

def get_latest():
  v =requests.get(UPDATE_URL)
  if v.status_code == 200:
    return v.text
  else:
    return False

def check_update():
  cur_version = torsurvey.get_version(semantic=True)
  latest_version = get_latest()
  print "Current version: %s" % cur_version
  print "Latest version : %s" % latest_version
  if latest_version:
    # @TODO compare versions
    print "New version available, run:"
    print " pip install -U torsurvey"
    print "to update or see the homepage for"
    print "more information: "
    print " http://www.github.com/nikcub/torsurvey/"
  return None