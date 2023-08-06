#!/usr/bin/env python
"""
Setup for SQLAlchemy backend for DM
"""
from setuptools import find_packages, setup

with open("README.md", "r") as fh:
    long_description = fh.read()

setup_params = dict(
    name="sqlalchemy_hcm_oracle",
    version='0.1',
    description="SQLAlchemy dialect for oracle special for hcm",
    author="tangrj",
    author_email="tangrj@inspur.com",
    keywords='oracle hcm SQLAlchemy',
    packages=find_packages(),
    include_package_data=True,
    entry_points={
        "sqlalchemy.dialects":
            ["HCMoracle = sqlalchemy_oracle.cx_oracle:OracleDialect_cx_oracle", "HCMoracle.cx_oracle = sqlalchemy_oracle.cx_oracle:OracleDialect_cx_oracle"]
    },
    install_requires=['sqlalchemy'],
)

if __name__ == '__main__':
    setup(**setup_params)
