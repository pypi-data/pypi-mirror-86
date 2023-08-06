__author__ = "Bo Pan"

from setuptools import setup, find_packages

with open("./cnabs_test/README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()


setup(name='cnabs_sdk_test',
      version='0.0.4', 
      description='CNABS OPENAPI SDK Test',
      author='Bo Pan', 
      author_email='bo.pan@cn-abs.com',
      url='https://github.com/cnabs',
      packages= [ "cnabs_test" ], 
      long_description=long_description,
      long_description_content_type="text/markdown", 
      license="GPLv3", 
      classifiers=[
          "Programming Language :: Python :: 3", 
          "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
          "Operating System :: OS Independent"],
      python_requires='>=3.3',
      install_requires=[
          "prettytable>=2.0.0",
          "cnabs-sdk>=0.0.4",
          ]
      )