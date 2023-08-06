import setuptools, os, sys

# if sys.platform == 'win32':
#     # make an .exe file beside the actual script
#     os.environ['SETUPTOOLS_LAUNCHER'] = "executable"

# read the contents of your README file
from os import path
this_directory = path.abspath(path.dirname(__file__))
with open(path.join(this_directory, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

setuptools.setup(
    name="slurm-jupyter",
    version="1.0.8",
    author="Kasper Munch",
    author_email="kaspermunch@birc.au.dk",
    description="Utility running jupyter on a slurm cluster.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/kaspermunch/slurm-jupyter",
    packages=setuptools.find_packages(),
    scripts=['slurm-jupyter.py', 'config-slurm-jupyter.sh'],
    # entry_points = {
    #     'console_scripts': ['slurm-jupyter=slurmjupyter.slurm_jupyter',
    #                         'config-slurm-jupyter=slurmjupyter.config_slurm_jupyter']
    # },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
    install_requires=[
          'colorama',
          'openssl',
    ])

# python3 setup.py sdist bdist_wheel
