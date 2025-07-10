from distutils.core import setup
from setuptools import find_packages
with open("README.rst", "r") as f:
    long_description = f.read()
setup(name='safeheron_api_sdk_python',
      version='1.1.17',
      description='Python for Safeheron API',
      long_description=long_description,
      author='safeheron',
      author_email='support@safeheron.com',
      url='https://github.com/Safeheron/safeheron-api-sdk-python',
      install_requires=[
            'pycryptodomex',
            'requests',
            'cryptography'
      ],
      license='MIT License',
      packages=[
            'safeheron_api_sdk_python',
            'safeheron_api_sdk_python.api',
            'safeheron_api_sdk_python.cosigner',
            'safeheron_api_sdk_python.webhook'
      ],
      platforms=["all"],
      classifiers=[
          'Operating System :: OS Independent',
          'Programming Language :: Python :: 3'
      ],
      )