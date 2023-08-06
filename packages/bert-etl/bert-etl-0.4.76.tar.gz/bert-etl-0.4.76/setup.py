import os
import sys

from setuptools import find_packages, setup

# Hacky, but functional
file_dir: str = os.path.dirname(__file__)
bert_path: str = os.path.join(file_dir, 'bert')
if not os.path.exists(bert_path):
    raise NotImplementedError

sys.path.append(file_dir)
import bert

# Always reference code-origin
# https://github.com/django/django/blob/master/setup.py#L7

CURRENT_PYTHON = sys.version_info[:2]
REQUIRED_PYTHON = (3, 6)

if CURRENT_PYTHON < REQUIRED_PYTHON:
    sys.stderr.write("""
==========================
Unsupported Python version
==========================
This version of bert-etl requires Python {}.{}, but you're trying to
install it on Python {}.{}.
This may be because you are using a version of pip that doesn't
understand the python_requires classifier. Make sure you
have pip >= 9.0 and setuptools >= 24.2, then try again:
    $ python -m pip install --upgrade pip setuptools
    $ python -m pip install bert
This will install the latest version of bert-etl which works on your
version of Python
""".format(*(REQUIRED_PYTHON + CURRENT_PYTHON)))
    sys.exit(1)


EXCLUDE_FROM_PACKAGES = ['bert.bin']
version = '0.4.76'
description = 'A microframework for simple ETL solutions'

def read(fname):
  with open(os.path.join(os.path.dirname(__file__), fname)) as f:
    return f.read()

setup(
    name='bert-etl',
    version=version,
    python_requires='>={}.{}'.format(*REQUIRED_PYTHON),
    url='https://github.com/jbcurtin/bert',
    author="Joseph Curtin <42@jbcurtin.io",
    author_email='bert@jbcurtin.io',
    description=description,
    long_description=read('README.md'),
    license='MIT',
    packages=find_packages(exclude=EXCLUDE_FROM_PACKAGES),
    include_package_data=True,
    scripts=[],
    install_requires=[
        'redis==3.3.5',
        'marshmallow==2.19.5',
        'boto3==1.9.251',
        'pyyaml==5.1.2',
        'GitPython==3.1.1',
    ],
    entry_points={
        'console_scripts': [
            'bert-example.py = bert.example.factory:run_from_cli',
            'bert-deploy.py = bert.deploy.factory:run_from_cli',
            'bert-runner.py = bert.runner.factory:run_from_cli',
            'bert-secrets.py = bert.secrets.factory:run_from_cli',
            'bert-roles.py = bert.roles.factory:run_from_cli',
            'bert-debug.py = bert.debug.factory:run_from_cli',
        ]
    },
    zip_safe=False,
    classifiers=[
    'Operating System :: OS Independent',
    'Programming Language :: Python',
    'Programming Language :: Python :: 3',
    'Programming Language :: Python :: 3.6',
    'Programming Language :: Python :: 3.7',
    'Programming Language :: Python :: 3.8',
    'Programming Language :: Python :: 3.9',
    'Programming Language :: Python :: 3 :: Only',
  ],
  project_urls={}
)

