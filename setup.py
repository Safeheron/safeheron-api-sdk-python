from distutils.core import setup
from setuptools import find_packages
with open("README.rst", "r") as f:
    long_description = f.read()
setup(name='safeheron_api_sdk_python',
      version='1.0.3',
      description='Python for Safeheron API',
      long_description=long_description,
      author='safeheron',
      author_email='support@safeheron.com',
      url='https://github.com/Safeheron/safeheron-api-sdk-python',
      install_requires=[],
      license='MIT License',
      packages=find_packages(),
      platforms=["all"],
      classifiers=[
          'Operating System :: OS Independent',
          'Programming Language :: Python :: 3'
      ],
      )