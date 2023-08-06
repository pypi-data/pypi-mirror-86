from setuptools import setup, Extension, find_packages
from Cython.Build import cythonize

ext = Extension(
        name='xwHash', 
        sources=['src/xhashes.cpp', 
                 'src/City.cpp', 
                 'src/MurmurHash3.cpp', 
                 'src/xwCHash.pyx'], 
        language='c++')

#setup(ext_modules=cythonize(ext))

#install_deps = ['numpy', 'cython>=0.24.1']
install_deps = []
test_deps = ['coverage>=4.0.3', 'pytest>=3.0', ]

setup(name='xwHash',
      version       = '0.0.2',
      description   = 'hashes from c++ libary',
      author        = 'vicky xiao',
      author_email  = 'xwq20080101@gmail.com',
      url           = '',
      packages      = find_packages(),
      #packages      = ['src'],
      ext_modules   = cythonize(ext),
      install_requires= install_deps,
      tests_require = test_deps)
