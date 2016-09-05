import os
from setuptools import setup

# Utility function to read the README file.
# Used for the long_description.  It's nice, because now 1) we have a top level
# README file and 2) it's easier to type in the README file than to put a raw
# string in below ...
def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()
	
setup(
    name='container_decrypter',
    version='1.2',
    packages=['container_decrypter'],
    url='https://github.com/dennisfischer/container_decrypter',
    license='MIT',
    author='Dennis Fischer',
    author_email='dennis.fischer@live.com',
    description='A library for decrypting JDownloader container formats. Currently it supports only DLC files. ',
	install_requires=[
		"requests"
	],
	test_suite="tests",
	long_description=read('README.md'),
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Topic :: Utilities",
        "License :: OSI Approved :: MIT License",
    ],
)
