import sys

import click

from pip_madison.utils import get_available_versions_files_and_urls, get_index_urls, star_credentials_url


# print(sys.argv)
# class DefaultCommandGroup(click.Group):
#     ignore_unknown_options = True
#     """allow a default command for a group"""
#     def format_help(self, ctx, formatter):
#         default_cmd = self.commands[self.default_command]
#         default_cmd.format_help(ctx, formatter)
#     # def get_params(self,ctx,args):
#
#     # def parse_args(self, ctx, args):
#     #     ctx.args = self.commands[self.default_command].parse_args(ctx,args)
#     #     return ctx.args
#     def command(self, *args, **kwargs):
#         default_command = kwargs.pop('default_command', False)
#         if default_command and not args:
#             kwargs['name'] = kwargs.get('name', '<>')
#         decorator = super(
#             DefaultCommandGroup, self).command(*args, **kwargs)
#
#         if default_command:
#             def new_decorator(f):
#                 cmd = decorator(f)
#                 self.default_command = cmd.name
#                 return cmd
#
#             return new_decorator
#
#         return decorator
#     # def list_commands(self, ctx):
#     #     #return ctx.invoke(list_versions)
#     #     return ['a','b']
#     def resolve_command(self, ctx, args):
#         print("R:",args)
#         try:
#             # test if the command parses
#             # args = [getattr(a,'encode',lambda x:a)('utf8') for a in args]
#             return super(
#                 DefaultCommandGroup, self).resolve_command(ctx, args)
#         except click.UsageError:
#             # command did not parse, assume it is the default command
#             print("Fall back on DEFAULT")
#             args.insert(0, self.default_command)
#             return super(
#                 DefaultCommandGroup, self).resolve_command(ctx, args)


@click.group()
@click.pass_context
def cli(ctx):
    pass
@cli.command("help",help="get some help")
@click.argument("topic",type=click.Choice(["format","python","os","types"],case_sensitive=False))
@click.pass_context
def show_help2(ctx,topic):
    help_text = {
        "format":"""
The `--format` flag allows the user to specify the format, by default the `--format`="{ver}| {fname}"    
       
    Available Format Variables
      * {ver} - the string representation of the version (eg. '1.19.4') 
      * {fname} - the string representation of the version ('numpy-1.19.4-cp39-cp39-win_amd64.whl')
      * {uri} - eg. 'https://files.pythonhosted.org/packages/.../numpy-1.19.4-cp39-cp39-win_amd64.whl#sha256=...'
      * {index-url} - eg 'https://pypi.org/simple'
      * {package_name} - eg. 'numpy' 
    Example Usage: 
      $ pip-madison --format "{ver}" numpy
      $ pip-madison --format="{fname}" numpy 
      $ pip-madison -f "{fname}" numpy
        """,
        "python":"""
the '--py' flag is used to specify a PYPI PYTHON CODE as spelled out below

the format is ppXY where pp is the 2 letter python code below , XY is the version (eg 27=2.7,36=3.6,etc)

you can ignore this by simply not providing it

    CODES
      * py  - generic python code ... im not sure if its ever used
      * cp  - cPython, this is standard python
      * ip  - ironPython
      * pp  - PyPy Python
      * jy  - Jython
    Examples:
      $ pip-madison --py cp35 numpy
      1.18.5| numpy-1.18.5-cp35-cp35m-win_amd64.whl
      $ pip-madison --py cp36 numpy
      1.19.4| numpy-1.19.4-cp36-cp36m-win_amd64.whl
        """,
        "types":"""
the '--type' flag allows you to specify a specific package type, you can combine multiple types with '|'

    VALID VALUES:
      * .zip
      * .tar.gz
      * .whl
      * .exe
      
    Example Useage:
      # this is the default '--type' find all zip or .tar.gz  
      $ pip-madison --type .zip --type .tar.gz --latest numpy  # default
      1.19.4| numpy-1.19.4.zip
       
      # if we only got .tar.gz that might be a bummer
      $ pip-madison --type .tar.gz --latest numpy  # default
      numpy-1.12.0b1.tar.gz
      
      # only wheels ... SHOULD REALLY specify python version and os
      $ pip-madison --type .whl --latest numpy
      1.19.4| numpy-1.19.4-pp36-pypy36_pp73-manylinux2010_x86_64.whl
      #WAIT WHAT???? HMMMM????? pp???? (see above comment)
       
      # get the whl for latest numpy for windows cPython
      $ pip-madison --type .whl --py cp37 --os win --latest numpy   
      numpy-1.19.4-cp37-cp37m-win_amd64.whl
      $ pip-madison --type .whl --py cp37 --os win32 --latest numpy   
      numpy-1.19.4-cp37-cp37m-win32.whl    
        """,
        "os":"""
the '--os' flag allows you to filter for a specific os type (really only applies to wheels)
by default `--os`='any' , you may alternatively use '-a' to specify

    Available Values:
       - any                                  # whatever ... (default value)
       - win, win32, win64                    # windows, windows x86, windows x64
       - linux, linux32, linux64              # linux any, linux x86, linux x64
       - darwin, darwin32, darwin64           # MACOS, MACOS x86, MACOS x64
       - other <<OS_TYPE>>_<<architecture>>   # CUSTOMIZE IT

    Example Usage:
      $ pip-madison --os win --type .whl numpy --latest # match any windows
      1.19.4| numpy-1.19.4-cp39-cp39-win_amd64.whl
      $ pip-madison --a win32 --type .whl numpy --latest # specify win32
      1.19.4| numpy-1.19.4-cp39-cp39-win32.whl
      $ pip-madison --os linux --type .whl numpy --latest # specify any linux
      1.19.4| numpy-1.19.4-cp39-cp39-manylinux2014_aarch64.whl
      $ pip-madison --os linux32 --type .whl numpy --latest # specify any linux
      1.19.4| numpy-1.19.4-cp39-cp39-manylinux2010_x86_64.whl
      $ pip-madison --os linux2014_aarch64 --type .whl numpy --latest # super specific!
      numpy-1.19.4-cp39-cp39-manylinux2014_aarch64.whl
    
        
        """
    }[topic.lower()]
    print(help_text)
@cli.command("madison",help="PACAKAGE_NAME is the name of the package to inspect, you can optionally include specific pypi indexes to search\n\n  eg. `$ pip-madison numpy https://user:passwd@my.pypi.org/simple`")
@click.argument("package_name")
@click.option("-r","--repository",multiple=True,default=get_index_urls,
              help="optionally supply one or more repositories to search (can be used multiple times)")
@click.option("-q","--quiet",is_flag=True,default=False,help="only print the version numbers (equivelent to --format \"{ver}\")")
@click.option("--latest",is_flag=True,default=False,help="if set only print the latest version")
@click.option("-t","--type",default=[".tar.gz",".zip"],multiple=True,type=click.Choice([".tar.gz",".zip",".whl",".exe"], case_sensitive=False),
              help="the fileType to search for. see also `pip-madison help types`")
@click.option("--py",default=None,required=False,metavar="PY_CODE",
              help="the pip format python version to check. see `pip-madison help python`")
@click.option("-a","--os", default=None, required=False,
              type=click.Choice(
                  ['win32','darwin32', 'linux32',
                   'win64', 'darwin64', 'linux64',
                   'win','darwin','linux',
                   'any'],

                  case_sensitive=False
              ),metavar="OS_CODE",
              help="the operating system to check against.\n\n see also `pip-madison help os`")

@click.option("-f","--format",type=str,
              help="the format to use: see `pip-madison help format`",
              default="{ver}| {fname}")
def list_versions(**kwargs):
    package_name = kwargs.get('package_name')
    if not kwargs.get("quiet", False):
        print("Looking For: {0}".format(package_name))

    endswith = "|".join(sorted(kwargs.get('type',['.zip','.tar.gz']),reverse=True,key=len))
    for pypa_url in kwargs.get('repository'):
        if not kwargs.get("quiet",False):
            print("Looking In: {0}".format(star_credentials_url(pypa_url)))

        data = get_available_versions_files_and_urls(pypa_url+"/%s/"%package_name.replace("_","-"),
                                                     kwargs.get('py',None),kwargs.get('os',None),
                                                     endswith)
        if data:
            if not kwargs.get("quiet",False):
                print("  {1} for: {0}".format(package_name,
                                              "List Versions" if not kwargs.get("latest",False) else "Latest Version")
                      )
            for entry in data:
                print("    %s"%kwargs.get("format","{ver}| {fname}").format(**entry))
                if kwargs.get("latest",False):
                    break
        else:
            if not kwargs.get("quiet", False):
                print("  No Versions of %s found"%package_name)

if __name__ == "__main__":
    cli()
