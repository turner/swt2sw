from setuptools import setup, find_packages

setup(
    name='my_package',
    version='0.1',
    packages=find_packages(),
    description='A description of your project',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    install_requires=[
        'numpy',
        'h5py'
    ],
    entry_points={
        'console_scripts': [
            'sw2swb=sw2swb.sw2swb:main',
        ],
    },
)
