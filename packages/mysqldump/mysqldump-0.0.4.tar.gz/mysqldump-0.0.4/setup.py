from setuptools import setup, find_packages
from os import path

curr_dir = path.abspath(path.dirname(__file__))

with open(path.join(curr_dir, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()
 
classifiers = [
  'Development Status :: 4 - Beta',
  'Intended Audience :: Education',
  'Operating System :: POSIX :: Linux',
  'License :: OSI Approved :: MIT License',
  'Programming Language :: Python :: 3'
]
 
setup(
  name='mysqldump',
  version='0.0.4',
  description='Mysqldump is a django package that is used to generate the logical backup of the MySQL database',
  long_description= long_description,
  long_description_content_type='text/markdown',
  url='',  
  author='Nandhakumar D',
  author_email='dnandhakumars@gmail.com',
  license='MIT', 
  classifiers=classifiers,
  keywords='mysqldump', 
  include_package_data=True,
  packages=find_packages(),
  install_requires=['django>=3.0']
)