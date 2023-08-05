
with open('README.txt', encoding='utf-8') as r_file:
    print(*r_file)

from setuptools import setup

setup(name='Practice number 6',
      version='0.1',
      packages=['package'],
      author_email='prudkoart@gmail.com',
      zip_safe=False)