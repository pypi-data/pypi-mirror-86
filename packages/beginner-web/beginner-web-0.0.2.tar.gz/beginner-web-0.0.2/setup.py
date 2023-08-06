# -*- coding:utf-8 -*-

import setuptools

with open(r'D:\Python Project\Packages\self\beginner-web\README.md', 'r') as fh:
    long_description = fh.read()

setuptools.setup(
    name='beginner-web',
    version='0.0.2',
    author='Dreambuilder4028',
    author_email='jiade_student@163.com',
    description='Python package to let beginners in Python have their website more easily.',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url=r'https://github.com/Dreambuilder4028/coder/commit/e15128f3440ebba64523b68c1134251805bd2395',
    packages=setuptools.find_packages(),
    classifiers=[
        'Programming Language :: Python :: 3',
        'Operating System :: OS Independent',
    ],
    install_requires=[],
)
