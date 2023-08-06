from setuptools import setup

from os import path

this_directory = path.abspath(path.dirname(__file__))
readfile = path.join(this_directory,'pipREADME.md')
if path.exists(readfile):
        with open(path.join(this_directory, 'pipREADME.md')) as f:
                long_description = f.read()
else:
        long_description = '''
        # essHIC
        ---

        ### A python package to analyze Hi-C matrices, enhance their specific patterns through spectral filtering and compute metric distances between couples of experiments.

        ---

        You may find the github repository at [https://github.com/stefanofranzini/essHIC](https://github.com/stefanofranzini/essHIC)

        ---

        #### essHIC contains many useful modules to guide users throughout the analysis:

        - [essHIC.makehic](https://github.com/stefanofranzini/essHIC/wiki/essHIC.make_hic): enables the user to process raw matrix data and their metadata to merge multiple sources into a single well ordered data repository, split chromosomes and obtain Observed over Expected matrices if needed.

        - [essHIC.hic](https://github.com/stefanofranzini/essHIC/wiki/essHIC.hic): wrapper class for Hi-C matrices containing metadata along with the matrix of contact probabilities for the chosen experiment. It contains useful tools
        to normalize and clean the matrix, compute its spectral properties, and process it to obtain its essential component. It also provides plotting functions to
        obtain high quality pictures with minimal knowledge of the matplotlib library.

        - [essHIC.ess](https://github.com/stefanofranzini/essHIC/wiki/essHIC.ess): tool to compute a dataset-wide distance matrix between all couples of experiments using the essential metric distance.

        - [essHIC.dist](https://github.com/stefanofranzini/essHIC/wiki/essHIC.dist): a useful explorative tool to analyze distance matrices. It allows to perform hierarchical and spectral clustering on the dataset, to compute the ROC curves according to the cell-types provided in the metadata, and to perform multiscaling dimensional reduction (MDS). It also contains plotting tools to visualize
        the results of all mentioned analyses.

        More information is available on the package [wiki](https://github.com/stefanofranzini/essHIC/wiki).

        ---

        ## INSTALLING

        essHIC is written in python, it has been tested in python2.7. Both the python3 language and the required packages need to be installed. To install the package through the python package manager, copy and paste the snippet below in your terminal:

        ```bash
        pip install --upgrade essHIC 
        ```

        Please notice that you may need to have administrator priviliges in order to be able to install the package. Using this method will take care of the dependencies.

        Otherwise, you may simply clone this repository to your computer. To use the package in a python script you will need to link its local path; to do so write the snippet below in your python code:

        ```python
        import sys

        sys.path.append('path/to/essHIC')

        import essHIC
        ```

        For *essHIC* to function correctly you will need to install the required dependencies:

        ```bash
        numpy
        scipy
        sklearn
        matplotlib
        ```

        ---

        ## USAGE

        To use *essHIC* in one of your python scripts import the package with

        ```python
        import essHIC
        ```

        for more information on how to use essHIC, please refer to the [tutorial](https://github.com/stefanofranzini/essHIC/wiki/tutorial) on the package [wiki](https://github.com/stefanofranzini/essHIC/wiki)
        '''

setup(name='essHIC',
      version='1.43',
      description='essHIC is a python module to compare HiC matrices by computing a metric distance between them',
      url='https://github.com/stefanofranzini/essHIC',
      author='Stefano Franzini',
      author_email='sfranzin@sissa.it',
      license='MIT',
      packages=['essHIC'],
  install_requires=[
          'numpy',
          'scipy',
          'matplotlib',
          'sklearn'
      ],
      zip_safe=True,
      long_description=long_description,
      long_description_content_type='text/markdown',
      keywords=['HiC','distance','spectral'])
