try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

config = {
    'description': 'Python Swiss Army Knife: common utilities and helpers for boilerplate code',
    'author': 'Marc Carré',
    'url': 'https://github.com/marccarre/py_sar',
    'download_url': 'https://github.com/marccarre/py_sar',
    'author_email': 'carre.marc@gmail.com',
    'version': '0.1',
    'install_requires': ['nose'],
    'packages': ['py_sar'],
    'scripts': [],
    'name': 'py_sar'
}

setup(**config)
