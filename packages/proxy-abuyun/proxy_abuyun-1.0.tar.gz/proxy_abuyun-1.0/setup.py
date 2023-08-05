# -*- coding: utf-8 -*-
# @Time    : 2020/11/20 16:29
# @Author  : Navy

import setuptools

with open('README.md', 'r', encoding='utf-8') as f:
    long_description = f.read()

setuptools.setup(
    name="proxy_abuyun",
    version='1.0',
    author='navy',
    auther_email='haijun0422@gmail.com',
    description='proxy of abuyun',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='',
    packages=setuptools.find_packages(),

)
