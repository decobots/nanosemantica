from distutils.core import setup

from setuptools import find_packages

setup(
    name="nanosemantica_app",
    version='1.0',
    description='helps to find recepiese which are possible to prepare',
    author='Maria Pritchina',
    author_email='pritchina.m.i@gmail.com',
    packages=find_packages('src'),
    package_dir={"": "src"},
)