# coding=utf-8

from setuptools import setup, find_packages

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name='LarkBot',

    version="0.0.3",
    description=(
        'Python SDK of Feishu Bot'

    ),
    long_description=open('README.md', 'r').read(),
    long_description_content_type="text/markdown",
    author='xiehengjian',
    author_email='846188037@qq.com',
    maintainer='xiehengjian',
    maintainer_email='846188037@qq.com',
    license='MIT License',
    packages=find_packages(),
    platforms=["ubuntu", 'windows','macos'],
    url='https://github.com/xiehengjian/LarkBot',
    classifiers=[
        'Development Status :: 4 - Beta',
        'Operating System :: OS Independent',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python',
        'Programming Language :: Python :: Implementation',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Topic :: Software Development :: Libraries'
    ],
    install_requires=[
        'requests',
    ]
)

