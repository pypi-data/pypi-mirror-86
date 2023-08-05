# -*- coding: utf-8 -*-
import os
from setuptools import setup, find_packages

here = os.path.abspath(os.path.dirname(__file__))
with open(os.path.join(here, 'README.rst')) as f:
    README = f.read()

with open(os.path.join(here, 'requirements.txt')) as f:
    requires = f.read()

with open(os.path.join(here, 'CURRENT_VERSION')) as f:
    current_version = f.read().splitlines()[0].strip()

tests_require = [
    'WebTest >= 1.3.1',  # py3 compat
    'pytest',  # includes virtualenv
    'pytest-cov',
    ]

dev_require = [
    'libsass',
]

entry_points = {
    "paste.app_factory": "main = endi_oidc_provider:main",
    "console_scripts": [
        "oidc-manage=endi_oidc_provider.scripts.manager:manage"
    ]
}

setup(name='endi_oidc_provider',
      version=current_version,
      description='endi_oidc_provider',
      long_description=README,
      classifiers=[
          "Programming Language :: Python",
          "Framework :: Pyramid",
          "Topic :: Internet :: WWW/HTTP",
          "Topic :: Internet :: WWW/HTTP :: WSGI :: Application",
      ],
      author='',
      author_email='',
      url='',
      keywords='web wsgi bfg pylons pyramid',
      packages=find_packages(),
      include_package_data=True,
      zip_safe=False,
      extras_require={
          'testing': tests_require,
          'dev': dev_require,
      },
      install_requires=requires,
      entry_points=entry_points,
      )
