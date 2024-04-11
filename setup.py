from setuptools import setup, find_packages

setup(
    name='sw2swb',
    version='0.1',
    packages=find_packages(),
    description='Tool to convert Spacewalk text files (.sw) to binary files (.swb)',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    install_requires=[
        'hdf5-indexer',
        'numpy',
        'h5py'
    ],
    entry_points={
        'console_scripts': [
            'sw2swb=sw2swb.sw2swb:main',
        ],
    },
)
