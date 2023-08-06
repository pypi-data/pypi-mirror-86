import re
import sys

import js2py
from bs4 import BeautifulSoup
from requests import get


def main():
    if len(sys.argv) < 2:
        print(
            """
Usage: phbdl [url]
""")
    url = sys.argv[1]
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
    print(urls)


if __name__ == "__main__":
    main()
