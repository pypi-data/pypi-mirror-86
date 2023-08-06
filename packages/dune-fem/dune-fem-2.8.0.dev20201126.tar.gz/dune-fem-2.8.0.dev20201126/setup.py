import sys, os
from setuptools import find_packages
from skbuild import setup

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name="dune-fem",
    version="2.8.0.dev20201126",
    author="The Dune Core developers",
    author_email="dune-fem@lists.dune-project.org",
    description="A discretization module providing an implementation of mathematical abstractions to solve PDEs on parallel computers including local grid adaptivity, dynamic load balancing, and higher order discretization schemes",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://gitlab.dune-project.org/dune-fem/dune-fem",
    packages=find_packages(where="python"),
    package_dir={"": "python"},
    install_requires=['UFL == 2017.1.0', 'dune-grid >= 2.8.0.dev0'],
    classifiers=[
        "Programming Language :: C++",
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: GNU General Public License (GPL)",
    ],
    python_requires='>=3.4',
    cmake_args=[
        '-DBUILD_SHARED_LIBS=TRUE',
        '-DDUNE_ENABLE_PYTHONBINDINGS=TRUE',
        '-DDUNE_PYTHON_INSTALL_LOCATION=none',
        '-DDUNE_GRID_GRIDTYPE_SELECTOR=ON',
        '-DALLOW_CXXFLAGS_OVERWRITE=ON',
        '-DUSE_PTHREADS=ON',
        '-DCMAKE_BUILD_TYPE=Release',
        '-DCMAKE_DISABLE_FIND_PACKAGE_LATEX=TRUE',
        '-DCMAKE_DISABLE_DOCUMENTATION=TRUE',
        '-DINKSCAPE=FALSE',
        '-DCMAKE_INSTALL_RPATH='+sys.prefix+'/lib/',
        '-DCMAKE_MACOSX_RPATH=TRUE',
    ]
)
