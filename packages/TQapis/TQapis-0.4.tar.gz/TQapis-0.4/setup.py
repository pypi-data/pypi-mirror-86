from setuptools import setup
setup(name='TQapis',
version='0.4',
description='Python package to interact with TreasuryQuants.com APIs',
url='https://github.com/treasuryquants/TQPython',
author='Shahram Alavian',
author_email='shahram_alavian@yahoo.com',
maintainer='Tanmay Jain',
maintainer_email='tanmayjain.cs@gmail.com',
license='MIT', # if you want you can use "LICENSE.txt"
packages=['TQapis'],
zip_safe=False,
long_description=open('README.MD').read(),
long_description_content_type='text/markdown',
keywords =["Treasury", "Quant", "TreasuryQuants", "Swap", "Valuations", "Quantitative Finance"],
install_requires=[
    "requests"
])