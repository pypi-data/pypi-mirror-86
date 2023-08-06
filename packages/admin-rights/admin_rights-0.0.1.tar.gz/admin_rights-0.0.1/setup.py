from setuptools import setup, find_packages

with open("README.md", "r") as fh:
    long_description = fh.read()
 
classifiers = [
  'Development Status :: 5 - Production/Stable',
  'Intended Audience :: Education',
  'Operating System :: OS Independent',
  'License :: OSI Approved :: MIT License',
  'Programming Language :: Python :: 3',
  'Programming Language :: Python :: 3.6',
  'Programming Language :: Python :: 3.7'
]
 
setup(
  name='admin_rights',
  version='0.0.1',
  description='This is a function that takes an array of users as an argument and checks if the role is an admin',
  long_description=long_description,
  long_description_content_type="text/markdown",
  url='',  
  author='Harun Gachanja',
  author_email='arrotechdesign@gmail.com',
  license='MIT', 
  classifiers=classifiers,
  keywords='roles', 
  packages=find_packages(),
  install_requires=['flask-jwt-extended'] 
)