#!/usr/bin/env python
# coding: utf-8

from setuptools import setup


setup(
    name='h5db',
    version='0.0.4',
    author='Larryjianfeng',
    author_email='244060203@qq.com',
    url='https://www.zhihu.com/people/feifeiaphy',
    description=u'利用h5来做一个分布式的kv磁盘存储工具',
    packages=['h5db'],
    install_requires=['h5py'],
    entry_points={
        'console_scripts': [
        ]
    }
)