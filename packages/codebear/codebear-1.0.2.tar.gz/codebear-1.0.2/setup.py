from distutils.core import setup
from setuptools import find_packages

with open("README.rst", "r", encoding="utf8") as f:
    long_description = f.read()

setup(name='codebear',  # 包名
      version='1.0.2',  # 版本号
      description='A pygame role package',
      long_description=long_description,
      author='yyb',
      author_email='877665814@qq.com',
      install_requires=[],
      license='MIT',
      packages=find_packages(),
      platforms=["all"],
      classifiers=[
          'Intended Audience :: Developers',
          'Operating System :: OS Independent',
          'Natural Language :: Chinese (Simplified)',
          'Programming Language :: Python',
          'Programming Language :: Python :: 3.7',
          'Programming Language :: Python :: 3.8',
          'Topic :: Software Development :: Libraries'
      ],
      )
