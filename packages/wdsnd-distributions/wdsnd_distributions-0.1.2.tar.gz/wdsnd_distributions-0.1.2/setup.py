from setuptools import setup
from setuptools import find_packages

setup(name='wdsnd_distributions',
      author='Wouter ten Brink',
      version='0.1.2',
      description='Binomial and Gaussian distribution objects',
      long_description="""Package includes three classes:
      
      Parent: 
      Distribution
      
      Children:
      Gaussian
      Binomial

      Can be used to plot histograms, read data to calculate means and add two instances of a class.""",
      long_description_content_type='text/markdown',
      packages=['wdsnd_distributions'],
      zip_safe=False)