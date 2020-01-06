from setuptools import setup, find_packages

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(name='cohort_compare',
      version='0.3.01',
      description='A library of functions for comparing clinical cohorts to the populations of US counties',
      classifiers=[
        'Development Status :: 4 - Beta',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3.6',
        'Topic :: Scientific/Engineering :: Information Analysis',
        'Topic :: Scientific/Engineering :: Medical Science Apps.'
      ],
      long_description=long_description,
      long_description_content_type="text/markdown",
      keywords='clinical study cohort similarity mapping',
      url='https://github.com/matthew-c-lenert/cohort_compare',
      author='MC Lenert',
      author_email='matthew.c.lenert@gmail.com',
      license='MIT',
      packages=['cohort_compare'],
      package_data={
        'cohort_compare': ['data/County_Data_after_impute_after_scaling.csv', 'data/us-albers-counties.json']
        },
      install_requires=[
          'numpy>=1.15.0',
          'scipy',
          'sklearn',
          'matplotlib',
          'fiona>=1.8.6',
          'geopandas>=0.4.1',
          'descartes'
      ],
      zip_safe=False)

