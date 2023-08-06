import configparser
import os
import platform
import re
import sys
from pySystem import System
import bs4
import requests

from pip_madison._cli_util import os_to_re, pyversion_to_re
if len(sys.argv) > 1 and sys.argv[1] not in ["help","madison"]:
    sys.argv.insert(1,"madison")

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

def get_available_versions_files_and_urls(package_url, py=None,os=None,endswith=".tar.gz"):
    endswith=endswith.replace(".","\\.")
    package_index, package_name = filter(None, package_url.rsplit("/", 2))
    pattern = "%s-(?P<ver>(?P<major>\d+)\.(?P<minor>\d+)\.?(?P<build>\d+)?)"%package_name.replace("_","[-_]")
    endings = endswith.split("|")
    alt_endings = []
    if "\\.tar\\.gz" in endings:
        alt_endings.append("\\.tar\\.gz")
        endings.remove("\\.tar\\.gz")
    if "\\.zip" in endings:
        alt_endings.append("\\.zip")
        endings.remove("\\.zip")

    if len(endings):
        pattern2 = ".*-(?P<py>%s[^-]*?)"%pyversion_to_re(py)
        pattern2 +=".*-(?P<os>%s)"%os_to_re(os)
        if len(alt_endings):
            pattern += "(?:%s)?"%pattern2
        else:
            pattern += pattern2

    pattern+="(?P<ext>%s)"%endswith
    page = bs4.BeautifulSoup(requests.get(package_url).content, features="html.parser")
    #print(pattern)

    def mapper(ele):
        match = re.search(pattern, ele.text,re.I)

        if not match:
            return None
        else:
            def intOrNone(x):
                if x is None:
                    return -1
                return int(x)
            match = match.groupdict()
            measure = list(map(intOrNone, [match.get('major',-1),match.get('minor',-1),match.get('build',-1)]))
            details = {"list": measure, 'package_name':package_name,
                       'ver': match.get('ver',"??????"),
                       'os':match.get('os','any') or "any",
                       'py':match.get('py','any') or "any",
                       'fname': ele.text,
                       'error': 'false', 'uri': ele.attrs['href'],'index-url':package_index}
            return details

    def map_it(L):
        return map(mapper, L)

    data = sorted(filter(None,map_it(page.find_all("a"))), key=lambda x: x['list'], reverse=True)
    return data

def get_latest_package_details(package_url,endswith=".tar.gz"):
    data = get_available_versions_files_and_urls(package_url,endswith)[0]
    if data:
        return data[0]

