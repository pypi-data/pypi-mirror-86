#! /usr/bin/env python
# -*- coding: utf-8 -*-
import setuptools

setuptools.setup(
    name='restsql',
    version='0.1.25',
    description=(
        'RestSQL库。用json与数据库交互。'
    ),
    url='',
    long_description='restsql',
    author="venzozhang",
    author_email='',
    maintainer='oliverdding',
    maintainer_email='oliverdding@tencent.com',
    license='MIT License',
    packages=['restsql'],
    install_requires=[
        'bitarray==1.2.1',
        'certifi==2020.6.20',
        'chardet==3.0.4',
        'elasticsearch==7.9.1',
        'elasticsearch-dsl==7.3.0',
        'guppy==0.1.10',
        'idna==2.10',
        'impyla==0.16.3',
        'ipaddress==1.0.23',
        'mysqlclient==1.4.6',
        'numpy==1.16.5',
        'pandas==0.24.2',
        'peewee==3.13.3',
        'psycopg2-binary==2.8.4',
        'pycrypto==2.6.1',
        'python-dateutil==2.8.1',
        'pytz==2020.4',
        'requests==2.24.0',
        'six==1.15.0',
        'thrift==0.9.3',
        'urllib3==1.25.11'
    ],
    classifiers=[
        "Programming Language :: Python",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)
