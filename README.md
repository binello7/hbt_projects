# hbtprojects
Repository containig codes for projects carried out at HBT.

The repository uses:\
`Python 3.10.9 | packaged by conda-forge | (main, Jan 11 2023, 15:15:40) [MSC v.1916 64 bit (AMD64)] on win32`

## Install
The packages needed to run the codes in this repository should be installed in
a conda environment. To do this, first create the conda environment:\
`conda create --name hbtprojects python=3.10`

To install a new package use the command:\
`conda install PACKAGENAME --channel conda-forge`

To export the installed packages to a `requirements.txt` file run:\
`conda list -e > requirements.txt`

To install the packages listed in a `requirements.txt` file do:\
`conda install --file requirements.txt`
