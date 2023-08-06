
from setuptools import setup

with open('README.md', 'r') as f:
    long_description = f.read()

setup(name='libcfbf',
      version='0.4',
      description="An implementation of Microsoft's Compound File Binary Format",
      long_description=long_description,
      long_description_content_type='text/markdown',
      url='https://git.rcarz.net/bobc/libcfbf',
      author='Bob Carroll',
      author_email='bob.carroll@alum.rit.edu',
      py_modules=['libcfbf'],
      classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: GNU General Public License v2 (GPLv2)',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 3',
        'Topic :: Office/Business :: Office Suites',
        'Topic :: Software Development :: Libraries'])
