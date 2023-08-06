#!/usr/bin/env python3

import re
import sys
import argparse

import js2py
from bs4 import BeautifulSoup
from requests import get

usage = """
    phbdl <url>
"""
version = '0.1.7'


def main():

    if len(sys.argv) == 1:
        sys.argv.append('--help')

    parser = argparse.ArgumentParser(prog='phbdl', usage=usage)
    parser.add_argument('-v', '--version', action='version',
                        version=version, help='print the version number')
    parser.add_argument('url')
    args = parser.parse_args()

    url = args.url
    soup = BeautifulSoup(get(url).text, features="html.parser")

    scripts = '\n'.join(
        [each.contents[0] if each.contents and str(each.contents[0]).find('flashvars') != -1 else '' for each in soup.find_all('script')])

    scripts = scripts[: scripts.find('playerObjList')]

    re_res = re.search(r'"quality":\[.*?\]', scripts).group()
    qualities = re_res[re_res.find('[')+1: re_res.find(']')].split(',')

    scripts += r'const urls = {'
    for q in qualities:
        scripts += f'quality_{q}p: quality_{q}p,'
    scripts += r'}'

    urls = js2py.eval_js(scripts)
    for q, u in urls.to_dict().items():
        print(f'{q}:')
        print(f'{u}')
        print()


if __name__ == "__main__":
    main()
