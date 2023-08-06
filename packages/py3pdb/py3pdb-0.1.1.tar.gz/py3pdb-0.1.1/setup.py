from setuptools import setup

setup(
    name='py3pdb',
    version='0.1.1',
    description='A Python3 API for the RCSB Protein Data Bank (PDB).',
    author='Hao Xu',
    author_email='nyx0flower@gmail.com',
    url='https://github.com/NYXFLOWER/py3pdb',
    license='MIT License',
    packages=['py3pdb'],
    install_requires=[
        'biopython',
        'requests',
        'colorama',
    ],
    keywords=['protein', 'data', 'api', 'pdb', 'protein 3d structure', 'BLASTp'],
    include_package_data=True,
    classifiers=[
        'Intended Audience :: Science/Research',
        'Programming Language :: Python :: 3.8',
    ],
)