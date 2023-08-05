from setuptools import setup, find_packages
 
classifiers = [
  'Development Status :: 5 - Production/Stable',
  'Intended Audience :: Education',
  'Operating System :: Microsoft :: Windows :: Windows 10',
  'License :: OSI Approved :: MIT License',
  'Programming Language :: Python :: 3'
]
 
setup(
  name='smutylii',
  version='1.0',
  description='Plays sounds',
  long_description=open('README.txt').read() + '\n\n' + open('CHANGELOG.txt').read(),
  url='',  
  author='MoreAtharvaTheCuber',
  author_email='athcubes@gmail.com',
  license='MIT', 
  classifiers=classifiers,
  keywords='sound', 
  packages=find_packages(),
  install_requires=[''] 
)