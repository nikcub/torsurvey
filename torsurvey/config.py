#!/usr/bin/env python
"""
	torsurvey.config - config abstraction
"""

import os, logging, ConfigParser, subprocess
import appdirs, db

ad = appdirs.AppDirs("torsurvey", "torsurvey")
_parser = ConfigParser.SafeConfigParser(allow_no_value=True)

DB_NAME = 'sites.db'
CNF_NAME = 'Torsurvey'
CONFIG_DEFAULTS = {
	'app': {
		'dbpath': 'sites.db',
		},
	'proxy': {
		'type': 'socks5',
		'host': '127.0.0.1',
		'port': 9050
		},
	}
CONFIG_REQUIRED = {
	'app': ('dbpath'),
}

class BadConfig(Exception):
	pass

def first_run():
	path_config = get_conf_path()
	path_db = get_db_path()
	if not os.path.isdir(ad.user_data_dir):
		os.mkdir(ad.user_data_dir)
	if not os.path.isfile(path_config):
		logging.debug("Writing config at %s" % path_config)
		write_blank(path_config)
	if not os.path.isfile(path_db):
		logging.debug("Writing empty db at: %s" % path_db)
		db = db.DbManager(path_db)
		db.init()

def clear_userdata():
	path_config = get_conf_path()
	path_db = get_db_path()
	conf_files = [path_config, path_db]
	for conf_file in conf_files:
		if os.path.isfile(conf_file):
			os.unlink(conf_file)

def get_db_path():
	return os.path.join(ad.user_data_dir, DB_NAME)

def get_conf_path():
	return os.path.join(ad.user_data_dir, CNF_NAME)

def defaults_write(parser):
	for default_section in CONFIG_DEFAULTS.keys():
		if not parser.has_section(default_section):
			parser.add_section(default_section)
		for key in CONFIG_DEFAULTS[default_section]:
			if not parser.has_option(default_section, key):
				parser.set(default_section, key, CONFIG_DEFAULTS[default_section][key])
	return parser

def defaults_check(parser):
	for section in CONFIG_REQUIRED.keys():
		if not parser.has_section(section):
			raise BadConfig("Require %s section in config" % section)
			parser.add_section(section)
		for i in CONFIG_REQUIRED[section]:
			if not parser.has_option(section, i):
				raise BadConfig("Require %s option in %s section of config" % (i, section))
			if len(parser.get(section, i)) < 1:
				raise BadConfig("Require non-empty %s option in %s section of config" % (i, section))
	return parser

def write_blank(file_path):
	"""Writes a blank config file at path provided by appdir"""
	global _parser
	_parser = defaults_write(_parser)
	write_config()

def write_config():
	path_config = get_conf_path()
	with open(path_config, 'wb') as cf:
		_parser.write(cf)
	logging.info("Config file written to %s" % path_config)

def edit_config():
	"""Edit config file in path from appdir"""
	path_config = get_conf_path()
	editor = os.environ.get('EDITOR','vim')
	subprocess.call([editor, path_config])
	return True

def get_config():
	_parser.read(get_conf_path())
	try:
		defaults_check(_parser)
	except BadConfig, e:
		logging.error(str(e))
	return _parser

def list():
	parser = get_config()
	for section in parser.sections():
		for (n, v) in parser.items(section):
			cprint("%s.%s" % (section, n))
	return True

def parse_name(name):
	try:
		section, cname = name.split('.', 1)
		if not section or not cname:
			raise IndexError
	except (IndexError, ValueError):
		logging.error("Invalid config option: %s" % name)
		return None, None
	parser = get_config()
	if not parser.has_section(section):
		logging.error("No such config section: %s" % section)
		return None, None
	if not parser.has_option(section, cname):
		logging.error("No such config option: %s" % name)
		return None, None
	return section, cname

def cprint(name):
	section, cname = parse_name(name)
	cval = get(name)
	print "%s.%s=%s" % (section, cname, cval)

def get(name):
	"""get a config option. format = section.name"""
	section, cname = parse_name(name)
	if not section or not cname:
		return False
	parser = get_config()
	return parser.get(section, cname)

def set(name, value):
	"""set a config option. format = section.name"""
	section, cname = parse_name(name)
	if not section or not cname:
		return False
	parser = get_config()
	parser.set(section, cname, value)
	write_config()
	return True
