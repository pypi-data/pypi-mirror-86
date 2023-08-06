import sys

import click

from pip_madison.utils import get_available_versions_files_and_urls, get_index_urls, star_credentials_url


@click.command("madison",help="PACAKAGE is the name of the package to inspect, you can optionally include specific pypi indexes to search\n\n  eg. `$ pip-madison numpy https://user:passwd@my.pypi.org/simple`")
@click.argument("package_name")
@click.argument("pypa_uri",nargs=-1,default=None)
def list_versions(package_name,pypa_uri=None):
    if not pypa_uri:
        pypa_uri = get_index_urls()
    for pypa_url in pypa_uri:
        print("Looking In: {0}".format(star_credentials_url(pypa_url)))
        data = get_available_versions_files_and_urls(pypa_url+"/%s/"%package_name.replace("_","-"))
        if data:
            print("  List Versions for: {0}".format(package_name))
            for entry in data:
                print("    {ver}| {fname}".format(**entry))
        else:
            print("  No Versions of %s found"%package_name)

if __name__ == "__main__":
    list_versions()
