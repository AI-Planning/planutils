
import setuptools

# Will force a check on the packages setup
from planutils.package_installation import PACKAGES

with open("README.md", "r") as fh:
    long_description = fh.read()


console_scripts = ["planutils = planutils:main"]

# create entrypoints dynamically
import glob
import os.path
for d in glob.glob(os.path.join(os.path.dirname(__file__),"planutils/packages/*")):
    if not os.path.isdir(d):
        continue

    name = os.path.basename(d)
    if name == "TEMPLATE":
        continue

    name2 = name.replace("-","_")
    console_scripts.append(f"{name}=planutils.entrypoints:entrypoints.{name2}")


setuptools.setup(name='planutils',
    version='0.2.12',
    description='General library for setting up linux-based environments for developing, running, and evaluating planners.',
    long_description=long_description,
    long_description_content_type="text/markdown",
    url='https://github.com/AI-Planning/planutils',
    author='',
    author_email='',
    license='MIT',
    packages=['planutils'],
    entry_points={ 'console_scripts': console_scripts, },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: POSIX :: Linux",
    ],
    python_requires='>=3.6',
    include_package_data=True,
    zip_safe=False)
