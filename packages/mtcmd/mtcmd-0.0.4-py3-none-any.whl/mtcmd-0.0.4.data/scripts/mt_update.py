#!python


import pkg_resources
from subprocess import call

packages = [dist.project_name for dist in pkg_resources.working_set]
packages = [x for x in packages if x.startswith('mt')]
call("pip3 install  --upgrade " + ' '.join(packages), shell=True)
