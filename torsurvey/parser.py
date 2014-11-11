#!/usr/bin/env python

"""torsurvey.parser
"""

import argparse

def get_parser():
  parser = argparse.ArgumentParser(prog='torsurvey', description='torsurvey')

  parser.add_argument('-v', dest='verbose', action='store_true', help='verbose output')
  parser.add_argument('-d', dest='debug', action='store_true', help='debug output (Warning: lots of output, for developers)')
  parser.add_argument('--proxy', dest='proxy', type=str, default=False, help='proxy string')
  parser.add_argument('--proxy_host', dest='proxy_host', default='127.0.0.1', type=str, help='proxy host (default: 127.0.0.1')
  parser.add_argument('--proxy_port', dest='proxy_port', default=9050, type=int, help='proxy port (default: 9050)')
  parser.add_argument('--proxy_type', dest='proxy_type', default='http', type=str, help='proxy type (default: http')
  parser.add_argument('--quiet', dest='quiet', action='store_true', help='quite (only error output)')
  parser.add_argument('--timeout', dest='timeout', type=int, default=10, help='connection timeout')

  subparsers = parser.add_subparsers(description='available subcommands', dest="command")

  parser_config = subparsers.add_parser('fetch', help='fetch onion addresses from url')
  parser_config.add_argument('--no-insert', dest='noinsert', action='store_true', help='show only no insert')
  parser_config.add_argument('--cache', dest='cache', action='store_true', help='use request cache')
  parser_config.add_argument('url', type=str, help='option name', nargs='?')

  parser_config = subparsers.add_parser('read', help='read onion addresses from file')
  parser_config.add_argument('filepath', type=str, help='option name', nargs='?')

  parser_update = subparsers.add_parser('flushdb', help='clear database')

  parser_update = subparsers.add_parser('survey', help='survey onion sites in database')

  parser_update = subparsers.add_parser('list', help='list onion sites in database')


  parser_update = subparsers.add_parser('update', help='check for updates')

  parser_update = subparsers.add_parser('checkip', help='check ip')

  parser_version = subparsers.add_parser('version', help='show version')


  return parser.parse_args()