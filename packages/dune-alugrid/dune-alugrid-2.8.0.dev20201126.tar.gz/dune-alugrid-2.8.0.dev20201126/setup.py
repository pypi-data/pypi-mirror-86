import sys, os
from setuptools import find_packages
from skbuild import setup

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name="dune-alugrid",
    version="2.8.0.dev20201126",
    author="Robert Kloefkorn, Martin Alkaemper, Andreas Dedner and Martin Nolte",
    author_email="dune-devel@lists.dune-project.org",
    description="Module providing the DUNE grid interface for unstructured simplicial and cube grids in 2 and 3 space dimensions",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://gitlab.dune-project.org/extensions/dune-alugrid",
    packages=find_packages(where="python"),
    package_dir={"": "python"},
    install_requires=['dune-grid >= 2.8.0.dev0'],
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
