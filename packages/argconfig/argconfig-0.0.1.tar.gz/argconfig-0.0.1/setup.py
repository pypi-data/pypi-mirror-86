from setuptools import setup
import argconfig

long_description = open('README.md').read()

REQUIREMENTS = ['pyyaml', 
                'argparse']

CLASSIFIERS = ['Development Status :: 4 - Beta',
               'Intended Audience :: Developers',
               'License :: OSI Approved :: MIT License',
               'Programming Language :: Python']

setup(name='argconfig',
      version=argconfig.__version__,
      description='Argparse enhanced with a config file to overwrite code-based defaults',
      long_description=long_description,
      long_description_content_type="text/markdown",
      url='https://github.com/patrick-c-odriscoll/argconfig',
      author="Patrick C O'Driscoll",
      author_email='patrick.c.odriscoll@gmail.com',
      license='MIT',
      py_modules=['argconfig'],
      classifiers=CLASSIFIERS,
      install_requires=REQUIREMENTS,
      keywords='CLI configuration arguments parsing')
