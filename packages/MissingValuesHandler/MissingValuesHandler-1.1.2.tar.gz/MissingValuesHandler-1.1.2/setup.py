# -*- coding: utf-8 -*-
from distutils.core import setup
setup(
  name = 'MissingValuesHandler',         # How you named your package folder (MyLib)
  packages = ['MissingValuesHandler'],   # Chose the same as "name"
  version = '1.1.2',      # Start with a small number and increase it with every change you make
  license='MIT',        # Chose a license from here: https://help.github.com/articles/licensing-a-repository
  description = 'Automatic missing value replacement',   # Give a short description about your library
  author = 'AVOKANDOTO',                   # Type in your name
  author_email = 'yannavok2@gmail.com',      # Type in your E-Mail
  url = 'https://github.com/YA26/Missing_values_handler',   # Provide either the link to your github or to your website
  download_url = 'https://github.com/YA26/Missing_values_handler/archive/v_112.tar.gz',    # I explain this later on
  keywords = ['missing values', 'nan values', 'RandomForest', 'random forest imputer'],   # Keywords that define your package best
  install_requires=[            # I get to this in a second
          'scikit-learn',
          'tensorflow',
          'numpy',
          'pandas',
          'matplotlib',
          'progressbar',
          'DataTypeIdentifier',
      ],
  classifiers=[
    'Development Status :: 3 - Alpha',      # Chose either "3 - Alpha", "4 - Beta" or "5 - Production/Stable" as the current state of your package
    'Intended Audience :: Developers',      # Define that your audience are developers
    'Topic :: Software Development :: Build Tools',
    'License :: OSI Approved :: MIT License',   # Again, pick a license
    'Programming Language :: Python :: 3',      # Specify which pyhton versions that you want to support
    'Programming Language :: Python :: 3.4',
    'Programming Language :: Python :: 3.5',
    'Programming Language :: Python :: 3.6',
    'Programming Language :: Python :: 3.7',
  ],
)