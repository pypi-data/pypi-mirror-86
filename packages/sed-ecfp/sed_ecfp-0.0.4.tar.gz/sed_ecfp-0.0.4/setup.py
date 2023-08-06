import setuptools
from os import path as os_path

with open("README.md", "r") as fh:
    long_description = fh.read()
	
this_directory = os_path.abspath(os_path.dirname(__file__))
def read_file(filename):
    with open(os_path.join(this_directory, filename), encoding='utf-8') as f:
        long_description = f.read()
    return long_description
	
def read_requirements(filename):
    return [line.strip() for line in read_file(filename).splitlines()
            if not line.startswith('#')]
setuptools.setup(
    name="sed_ecfp", # Replace with your own username
    version="0.0.4",
    author="xhj",
    description="Predicting Bioactivities of Ligand Molecules Targeting G Protein-coupled Receptors by Merging Sparse Screening of Extended Connectivity Fingerprints and Deep Neural Nets",
    long_description=long_description,
    long_description_content_type="text/markdown",
    packages=['sed','sed\\data'],
	package_data={
		'':['*.csv']
	},
	install_requires=read_requirements('requirements.txt'),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.5',
)