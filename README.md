## Tor Survey

Scripts and tools to maintain a database of Tor hidden sites and crawl them for updates.

Current database contains 2313 Tor hidden sites.

## Requirements

 * `requesocks` - connect to Tor SOCKS server
 * `beautifulsoup` - pbparse hidden site data

## Install

```sh
$ git clone https://github.com/nikcub/torsurvey.git
$ cd torsurvey
$ pip install requirements.txt
```

## Usage

Help

``sh
$ ./torsurvey-cli --help
``

Command line options:

```
optional arguments:
  -h, --help            show this help message and exit
  -v                    verbose output
  -d                    debug output (Warning: lots of output, for developers)
  --proxy PROXY         proxy string
  --proxy_host PROXY_HOST
                        proxy host (default: 127.0.0.1
  --proxy_port PROXY_PORT
                        proxy port (default: 9050)
  --proxy_type PROXY_TYPE
                        proxy type (default: http
  --quiet               quite (only error output)
```

To add onion hosts extracted from a URL:

``sh
$ ./torsurvey-cli fetch http://url/
``

To add onion hosts extracted from a local file:

``sh
$ ./torsurvey-cli --help
``

List hosts in database:

``sh
$ ./torsurvey-cli list
``

Crawl database and update status, title, description and copy of page:

``sh
$ ./torsurvey-cli survey
``

## Updates

Send pull requests of `sites.db` if you add sites to the database

## Schema

``sql
sqlite> .schema sites
CREATE TABLE sites (id INTEGER primary key, host text unique on conflict ignore, schema text, title text, content blob, status, integer, checked integer, inserted integer, description text);
``