import os

from setuptools import setup

from src.PythonDebugTools import __version__, __classifiers__, __author__, __name__, __license__, __url__, __email__, __short_description__, __maintainer_email__, __maintainer__


with open(os.path.abspath("requirements.txt"), "r") as f:
    install_requires = f.readlines()

with open(os.path.abspath("README.md"), "r") as f:
    long_description = f.read()

data_files = [
        'PythonDebugTools/*.py'
        ]

setup(name=__name__,
      version=__version__,
      packages=[__name__],
      url=__url__,
      # download_url=f'https://github.com/Jakar510/PythonDebugTools/releases/tag/{version}',
      license=__license__ or 'GNU GENERAL PUBLIC LICENSE Version 3, 29 June 2007',
      author=__author__,
      author_email=__email__,
      maintainer=__maintainer__,
      maintainer_email=__maintainer_email__,
      description=__short_description__,
      long_description=long_description,
      long_description_content_type="text/markdown",
      install_requires=install_requires,
      classifiers=__classifiers__,
      keywords='switch switch-case case',
      package_dir={ 'PythonDebugTools': 'src/PythonDebugTools' },
      package_data={
              'PythonDebugTools': data_files,
              },
      )
