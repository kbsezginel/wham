"""
Python wrapper for Weighted Histogram Analysis Method as implemented by Grossfield et al.
-> http://membrane.urmc.rochester.edu/?page_id=126
"""
from setuptools import setup, find_packages


setup(
    name="wham",
    version="0.1.0",
    description="Python wrapper for Weighted Histogram Analysis Method as implemented by Grossfield et al.",
    author="Kutay B. Sezginel",
    author_email="kbs37@pitt.edu",
    url='https://github.com/kbsezginelwham',
    include_package_data=True,
    packages=find_packages(),
    install_requires=['numpy'],
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Science/Research',
        'Programming Language :: Python :: 3',
    ],
)
