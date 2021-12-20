
import setuptools

# Will force a check on the packages setup
from planutils.package_installation import PACKAGES

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(name='planutils',
      version='0.3.1',
      description='General library for setting up linux-based environments for developing, running, and evaluating planners.',
      long_description=long_description,
      long_description_content_type="text/markdown",
      url='https://github.com/AI-Planning/planutils',
      author='',
      author_email='',
      license='MIT',
      packages=['planutils'],
      scripts=['bin/planutils'],
      classifiers=[
          "Programming Language :: Python :: 3",
          "License :: OSI Approved :: MIT License",
          "Operating System :: POSIX :: Linux",
      ],
      python_requires='>=3.6',
      include_package_data=True,
      zip_safe=False)
