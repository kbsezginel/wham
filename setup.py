"""
Python wrapper for Weighted Histogram Analysis Method as implemented by Grossfield et al.
-> http://membrane.urmc.rochester.edu/?page_id=126
"""
from setuptools import setup, find_packages


setup(
    name="wham",
    version="0.1.1",
    description="Python wrapper for Weighted Histogram Analysis Method as implemented by Grossfield et al.",
    author="Kutay B. Sezginel, Brian Novak",
    url='https://github.com/bnovak1/wham',
    include_package_data=True,
    packages=find_packages(),
    install_requires=['numpy'],
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Science/Research',
        'Programming Language :: Python :: 3',
    ],
)
