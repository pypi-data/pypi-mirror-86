# -*- coding: utf-8 -*-
# License: 3-clause BSD
from setuptools import setup, find_namespace_packages
from setuptools.command.develop import develop
from setuptools.command.install import install
import subprocess

_MAJOR               = 0
_MINOR               = 9
_MICRO               = 5

version              = '%d.%d.%d' % (_MAJOR, _MINOR, _MICRO)
release              = '%d.%d' % (_MAJOR, _MINOR)

metainfo = {
    'authors': {"main": ("cokelaer", "thomas.cokelaer@pasteur.fr")},
    'version': version,
    'license' : 'new BSD',
    'url' : "http://github.com/sequana/",
    'description': "A variant calling pipeline to analyse sequencing Illumina data" ,
    'platforms' : ['Linux', 'Unix', 'MacOsX', 'Windows'],
    'keywords' : ['snakemake', "sequana", "NGS", "freebayes", "variant calling"],
    'classifiers' : [
          'Development Status :: 4 - Beta',
          #'Development Status :: 5 - Production/Stable',
          'Intended Audience :: Education',
          'Intended Audience :: End Users/Desktop',
          'Intended Audience :: Developers',
          'Intended Audience :: Science/Research',
          'License :: OSI Approved :: BSD License',
          'Operating System :: OS Independent',
          'Programming Language :: Python :: 3.5',
          'Programming Language :: Python :: 3.6',
          'Topic :: Software Development :: Libraries :: Python Modules',
          'Topic :: Scientific/Engineering :: Bio-Informatics',
          'Topic :: Scientific/Engineering :: Information Analysis',
          'Topic :: Scientific/Engineering :: Mathematics',
          'Topic :: Scientific/Engineering :: Physics']
    }

NAME = "variant_calling"

class Install(install):
    def run(self):
        cmd = "sequana_completion --name {} --force ".format(NAME)
        try: subprocess.run(cmd.split())
        except:pass
        install.run(self)

class Develop(develop):
    def run(self):
        cmd = "sequana_completion --name {} --force ".format(NAME)
        try:subprocess.run(cmd.split())
        except:pass
        develop.run(self)

setup(
    name             = "sequana_{}".format(NAME),
    version          = version,
    maintainer       = metainfo['authors']['main'][0],
    maintainer_email = metainfo['authors']['main'][1],
    author           = metainfo['authors']['main'][0],
    author_email     = metainfo['authors']['main'][1],
    long_description = open("README.rst").read(),
    keywords         = metainfo['keywords'],
    description      = metainfo['description'],
    license          = metainfo['license'],
    platforms        = metainfo['platforms'],
    url              = metainfo['url'],
    classifiers      = metainfo['classifiers'],

    # package installation
    packages = ["sequana_pipelines.variant_calling", 
        "sequana_pipelines.variant_calling.data"],

    install_requires = open("requirements.txt").read(),

    # This is recursive include of data files
    exclude_package_data = {"": ["__pycache__"]},
    package_data = {
        '': ['*.yaml', "*.rules", "*json", "requirements.txt", "*png"],
        'sequana_pipelines.variant_calling.fastqc.data' : ['*.*'], 
        },

    zip_safe=False,

    entry_points = {'console_scripts':[
        'sequana_pipelines_variant_calling=sequana_pipelines.variant_calling.main:main',
        'sequana_variant_calling=sequana_pipelines.variant_calling.main:main']
    }

)
