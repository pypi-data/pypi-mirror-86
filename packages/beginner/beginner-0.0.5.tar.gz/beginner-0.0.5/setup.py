# -*- coding:utf-8 -*-

import setuptools

with open(r'D:\Python Project\Packages\self\beginner\README.md', 'r') as fh:
    long_description = fh.read()

setuptools.setup(
    name='beginner',
    version='0.0.5',
    author='Dreambuilder4028',
    author_email='jiade_student@163.com',
    description='Python package to let beginners in Python studies more easily.',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://github.com/Dreambuilder4028/coder/',
    packages=setuptools.find_packages(),
    classifiers=[
        'Programming Language :: Python :: 3',
        'Operating System :: OS Independent',
    ],
    install_requires=[],
)
