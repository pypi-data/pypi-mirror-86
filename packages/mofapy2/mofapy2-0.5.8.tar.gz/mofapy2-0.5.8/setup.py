import sys
import os
from setuptools import setup
from setuptools import find_packages

exec(open(os.path.join(os.path.dirname(__file__), 'mofapy2', 'version.py')).read())

def setup_package():
  install_requires = ['pandas', 'scipy>=1.5.1', 'numpy', 'sklearn', 'argparse', 'h5py', 'dtw-python>=1.1.5']
  metadata = dict(
      name = 'mofapy2',
      version = __version__,
      description = 'Multi-Omics Factor Analysis v2, a statistical framework for the integration of multi-group and multi-omics data',
      url = 'http://github.com/bioFAM/MOFA2',
      author = 'Ricard Argelaguet <ricard.argelaguet@gmail.com>, Damien Arnol, Danila Bredikhin, Britta Velten <britta.velten@gmail.com>',
      license = 'LGPL-3.0',
      packages = find_packages(),
      install_requires = install_requires
    )

  setup(**metadata)


if __name__ == '__main__':
  if sys.version_info < (2,7):
    sys.exit('Sorry, Python < 2.7 is not supported')
    
  setup_package()


