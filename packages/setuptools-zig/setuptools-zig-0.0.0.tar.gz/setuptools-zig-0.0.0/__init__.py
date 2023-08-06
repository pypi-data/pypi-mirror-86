# coding: utf-8

from __future__ import print_function, absolute_import, division, unicode_literals

_package_data = dict(
    full_package_name="setuptools-zig",
    version_info=(0, 0, 0),
    __version__='0.0.0',
    author="Anthon van der Neut",
    author_email="a.van.der.neut@ruamel.eu",
    description="A setuptools extension for building cpython extensions written in zig.",
    keywords="setuptools zig",
    entry_points=None,
    license="Copyright Ruamel bvba 2020",
    since=2020,
    # status="α|β|stable",  # the package status on PyPI
    # data_files="",
    # universal=True,
    # install_requires=dict(),
    tox=dict(
        env='3',  # *->all p->pypy
    ),
)


version_info = _package_data['version_info']
__version__ = _package_data['__version__']
