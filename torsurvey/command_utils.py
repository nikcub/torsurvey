#!/usr/bin/env python

""" torsurvey - command_utils.py

Default command line utitlities to run torsurvey
"""

import os, sys, logging
import torsurvey, db, parser, updater, controller, torapi, config

def main(argv=[]):
  args = parser.get_parser()

  verbose = 1
  if args.verbose:
    verbose = 2
  if args.debug:
    verbose = 3

  if verbose>2:
    log_level=logging.DEBUG
  elif verbose==2:
    log_level=logging.INFO
  elif verbose==1:
    log_level=logging.WARNING
  elif verbose<1:
    log_level=logging.ERROR

  logging.basicConfig(level=log_level, format="%(asctime)s %(levelname)s: %(message)s")

  proxy = args.proxy
  proxy_host = args.proxy_host
  proxy_port = args.proxy_port
  proxy_type = args.proxy_type

  config.first_run()

  if args.command == 'version':
    print torsurvey.get_version()
    return True

  elif args.command == 'update':
    return updater.check_update()

  ac = torapi.TorAPI(proxy_host=proxy_host, proxy_port=proxy_port, proxy_type=proxy_type, timeout=args.timeout)
  dbi = db.DbManager(args.dbpath)
  dbi.init()
  tc = controller.TorController(ac, dbi)
  # cx = CexMethods(ac, dbi)

  if args.command == 'checkip':
    print "Checking IP address"
    print ac.get_ip()
    return True

  elif args.command == 'flushdb':
    dbi.flush()
    print "Cleared db"

  elif args.command == 'fetch':
    if not args.url:
      logging.error("URL to fetch from required")
      return False
    print "Fetching from %s " % args.url
    f = tc.fetch_sitelist(args.url, args.cache, (not args.noinsert))
    return True

  elif args.command == 'read':
    if not args.filepath:
      logging.error("Need file to read onion addresses from")
    f = tc.read_sitelist(args.filepath, (not args.noinsert))

  elif args.command == 'survey':
    tc.survey(args.deadonly)

  elif args.command == 'list':
    dbi.list()

def cl_error(msg=""):
  print >> sys.stderr, msg

def run_cl(argv=[]):
  try:
    raise SystemExit(main(sys.argv))
  except KeyboardInterrupt:
    cl_error('Interrupted.')
    raise SystemExit(-1)
