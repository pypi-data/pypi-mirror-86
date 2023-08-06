# -*- coding: utf-8 -*-
import re
import logging
from os.path import join, exists
from urllib.parse import urljoin

import click
import requests
from tqdm import tqdm
from bs4 import BeautifulSoup


logger = logging.getLogger(__name__)


DEFAULT_SERVER = 'http://libgen.rs/'
TORRENTS_URI = '/repository_torrent/'
TORRENT_PATTERN = re.compile(r'r_\d+\.torrent')


def parse_torrent_fns(torrents_html):
    soup = BeautifulSoup(torrents_html, 'html.parser')
    a_tags = soup.find_all('a')
    fns = []
    if not a_tags:
        return fns
    for a_tag in a_tags:
        href = a_tag.get('href', None)
        if href and TORRENT_PATTERN.search(href):
            fns.append(href)
    return fns


@click.command()
@click.option('-s', '--server', default=None, help='LibGen server, default is %s' % DEFAULT_SERVER)
@click.option('-p', '--proxy', default=None, help='proxy url, eg, http://localhost:1080, default no proxy')
@click.option('-o', '--outdir', default='.', help='output file directory, default is current directory')
@click.option('-v', '--verbose', is_flag=True, help='enable DEBUG mode')
def libgener_torrents(server, proxy, outdir, verbose):
    if verbose:
        logging.basicConfig(level=logging.DEBUG)
    if not server:
        server = DEFAULT_SERVER
    proxies = {'http': proxy, 'https': proxy} if proxy else None
    torrents_url = urljoin(server, TORRENTS_URI)
    torrents_response = requests.get(torrents_url, proxies=None)
    torrent_fns = parse_torrent_fns(torrents_response.text)
    for torrent_fn in tqdm(torrent_fns):
        torrent_file = join(outdir, torrent_fn)
        if exists(torrent_file):
            continue
        torrent_url = urljoin(server, TORRENTS_URI, torrent_fn)
        response = requests.get(torrent_url, proxies=proxies)
        if not response.ok:
            logger.warning('failed to download %s' % torrent_fn)
            continue
        with open(join(outdir, torrent_fn), 'wb') as fp:
            fp.write(response.content)
    return 0
