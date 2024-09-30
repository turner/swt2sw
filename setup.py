from setuptools import setup, find_packages

setup(
    name='swt2sw',
    version='1.0',
    packages=find_packages(),
    description='Tool to convert Spacewalk text files (.swt) to binary files (.sw)',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    install_requires=[
        'hdf5-indexer',
        'numpy',
        'h5py'
    ],
    entry_points={
        'console_scripts': [
            'swt2sw=swt2sw.swt2sw:main',
        ],
    },
)
