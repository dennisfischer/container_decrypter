import os
from setuptools import setup

setup(
    name='container_decrypter',
    version='1.3',
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
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Topic :: Utilities",
        "License :: OSI Approved :: MIT License",
    ],
)
