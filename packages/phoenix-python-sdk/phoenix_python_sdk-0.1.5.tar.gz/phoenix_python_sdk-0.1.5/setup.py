# -*- coding: utf-8 -*-

from distutils.core import setup
import setuptools

setup(
    name='phoenix_python_sdk',  # 包的名字
    version='0.1.5',  # 版本号
    description='发送消息',  # 描述

    packages=['phoenix_python_sdk'],  # 包内需要引用的文件夹

    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',  # BSD认证
        'Programming Language :: Python',  # 支持的语言
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',  # python版本 。。。
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Topic :: Software Development :: Libraries'
    ],
    zip_safe=True
)
