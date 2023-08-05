'''module to state PyCHAM package metadata'''
from setuptools import setup
from setuptools import find_packages


with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name="PyCHAM",
    version="2.1.3",
    author="Simon O'Meara",
    author_email="simon.omeara@manchester.ac.uk",
    description="PyCHAM: CHemistry with Aerosol Microphysics in Python",
    long_description=long_description,
    long_description_content_type="text/markdown",
    keywords=['aerosol','chamber','model'],
    url="https://github.com/simonom/PyCHAM",
    packages=find_packages(include=['PyCHAM', 'PyCHAM.*']),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
    
# state dependencies for PyCHAM, note that openbabel v3.1.1.1 didn't install via pip when tested on 19/11/2020
install_requires=["PyQt5","pickleshare","numpy","backcall","certifi","cycler","decorator","gitpython","ipdb","matplotlib","llvmlite","scipy","xmltodict","openbabel==2.4.0"]
)
