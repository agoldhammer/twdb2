from setuptools import setup, find_packages
setup(name="twdb2",
      version="0.1",
      scripts=['bin/query', 'bin/maketopics', 'bin/readfeed',
               'bin/readfeed.d', 'bin/storeauthtable'],
      packages=find_packages())
