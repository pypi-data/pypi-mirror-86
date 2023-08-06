import configparser
import os
import platform
import re
import sys
from pySystem import System
import bs4
import requests

def star_credentials_url(s):
    return re.sub("://([^/]*)@","://*****@",s)
def distinct_list(L):
    seen = set()
    return [i for i in L if i not in seen and not seen.add(i)]

def get_default_index_url():
    result = System().pip.install("-h")
    return re.search("\(default\s*([^\s\)]*)\)",result.split("\n  -i, --index-url")[1]).group(1)

def get_index_urls():
    result=System().pip.config.list()
    results = distinct_list(re.findall("index-url\s*='(.*)'\n",result))
    if "global.index-url=" not in result:
        default = get_default_index_url()
        results.append(default)
    return results



def get_extra_index_url(cfgPath=None):
    ## ON WINDOWS this file goes in C:\Users\<<USERNAME>>\AppData\Roaming\pip\pip.ini !!!!!
    ## ON Linux this file goes in /home/<<USERNAME>>/.config/pip/pip.conf !!!!!
    ## ON Mac $HOME/Library/Application Support/pip/pip.conf  **OR** $HOME/.config/pip/pip.conf
    #                                                                IFF folder pip is not in 'Application Support'
    if cfgPath is None:
        if platform.system() == "Windows":
            cfgPath = os.path.expanduser("~/AppData/Roaming/pip/pip.ini")
        elif platform.system() == "Linux":
            cfgPath = os.path.expanduser("~/.config/pip/pip.conf")
        elif platform.system() == "Darwin":
            cfgPath = os.path.expanduser("~/Library/Application Support/pip/pip.conf")
            if not os.path.exists(os.path.expanduser("~/Library/Application Support/pip")):
                cfgPath = os.path.expanduser("~/.config/pip/pip.conf")
    p = configparser.ConfigParser()
    p.read(cfgPath)
    return p['global'].get('extra-index-url')

def get_available_versions_files_and_urls(package_url, endswith=".tar.gz"):
    page = bs4.BeautifulSoup(requests.get(package_url).content, features="html.parser")
    def mapper(ele):
        match = re.search('(\d+)\.(\d+)\.(\d+)', ele.text)
        if not match:
            return {"list": [-1, -1, -1, -1], "ver": ele.text, 'fname': '', "error": True}
        else:
            measure = [1 if ele.text.endswith(".tar.gz") else 0] + list(map(int, match.groups()))
            details = {"list": measure, 'ver': ".".join(match.groups()), 'fname': ele.text,
                       'error': 'false', 'uri': ele.attrs['href']}
            return details

    def map_it(L):
        return map(mapper, L)

    data = sorted(map_it(page.find_all("a")), key=lambda x: x['list'], reverse=True)
    return [d for d in data if d['fname'].endswith(endswith) and not d.update({'list': d['list'][1:]})]
