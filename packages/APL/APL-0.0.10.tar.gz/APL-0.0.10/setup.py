from setuptools import setup, find_packages
 
classifiers = [
  'Development Status :: 5 - Production/Stable',
  'Intended Audience :: Education',
  'Operating System :: Microsoft :: Windows :: Windows 10',
  'License :: OSI Approved :: MIT License',
  'Programming Language :: Python :: 3'
]

setup(
  name='APL',
  version='0.0.10',
  description="A library includes my important funcs",
  long_description="A library includes my important funcs",
  url='https://www.youtube.com/channel/UCknfQGHQG0iXJVLOwijKdRA',  
  author='Ahmad Draie',
  author_email='ahmaddraa2000@gmail.com',
  license='MIT', 
  classifiers=classifiers,
  keywords='a lot of things', 
  packages=find_packages(),
  install_requires=[''] 
)