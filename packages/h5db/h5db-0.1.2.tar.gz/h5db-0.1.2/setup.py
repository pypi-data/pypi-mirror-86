#!/usr/bin/env python
# coding: utf-8

from setuptools import setup


with open("README.rst", "r") as fh:
    long_description = fh.read()


setup(
    name='h5db',
    version='0.1.2',
    author='Larryjianfeng',
    author_email='244060203@qq.com',
    url='https://www.zhihu.com/people/feifeiaphy',
    description=u'利用h5来做一个分布式的kv磁盘存储工具',
    long_description=long_description,
    long_description_content_type="text/x-rst",
    packages=['h5db'],
    install_requires=['h5py'],
    entry_points={
        'console_scripts': [
        ]
    }
)