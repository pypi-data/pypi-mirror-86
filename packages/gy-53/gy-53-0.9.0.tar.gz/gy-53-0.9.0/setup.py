# coding: utf-8

from setuptools import setup, find_packages

setup(
    name='gy-53',
    version='0.9.0',
    author='idevlab',
    author_email='idevlab@outlook.com',
    license='MIT License',
    url='https://github.com/ichendev/gy-53',
    description=u'GY-53 ToF lib',
    packages=find_packages(),
    install_requires=['pyserial'],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)
