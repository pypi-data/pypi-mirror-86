import os
import sys
from setuptools import setup, find_packages
from setuptools.command.install import install
from jupyterhub_singleuser_profiles import version as singleuser_profiles_version
import distutils.log

def copy_dir():
    dir_path = 'ui'
    for (dirpath, dirnames, files) in os.walk(dir_path):
        try:
            print(os.path.join(dirpath.split('/', 1)[1]))
            yield os.path.join(dirpath.split('/', 1)[1], '*')
        except Exception:
            print(dirpath)

def get_install_requires():
    with open('requirements.txt', 'r') as requirements_file:
        # TODO: respect hashes in requirements.txt file
        res = requirements_file.readlines()
        return [req.split(' ', maxsplit=1)[0] for req in res if req]

setup(
    name='jupyterhub-singleuser-profiles',
    version=singleuser_profiles_version.__version__,
    description='A tool to parse yaml configuration files used in singleuser JupyterHub servers',
    long_description='A tool to parse yaml configuration files used in singleuser JupyterHub servers',
    author='Vaclav Pavlin',
    author_email='vasek@redhat.com',
    license='GPLv3+',
    packages = find_packages(),
    entry_points = {
              'console_scripts': [
                  'jupyterhub-singleuser-profiles-api = jupyterhub_singleuser_profiles.api.api:main',                  
              ],              
          },
    zip_safe=False,
    install_requires=get_install_requires(),
    include_package_data=True,
)
