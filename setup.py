try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

config = {
    'name': 'py_sar',
    'packages': ['py_sar'],
    'install_requires': ['nose'],
    'version': '0.1',
    'description': 'Python Swiss Army Knife: common utilities and helpers for boilerplate code',
    'author': 'Marc Carré',
    'author_email': 'carre.marc@gmail.com',
    'url': 'https://github.com/marccarre/py_sar',
    'download_url': 'https://github.com/marccarre/py_sar',
    'keywords': ['common', 'utilities', 'utility', 'utils', 'util', 'helpers', 'helper', 'input validation', 'validation'],
}

setup(**config)
