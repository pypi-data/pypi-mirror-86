from distutils.core import setup

setup(
    name = 'debtsum',
    packages = ['debtsum'],
    version = '1.0.0',
    license='MIT',
    description = 'A tool that allows to summarize medic mobile debt files',
    author = 'Elias W. BA',
    author_email = 'eliaswalyba@gmail.com',
    url = 'https://github.com/eliaswalyba/debtsum',
    download_url = 'https://github.com/eliaswalyba/debtsum/archive/v1.0.0.tar.gz',
    keywords = ['DEBT', 'SUMMARIZE', 'PYTHON'],
    install_requires=[
        'pandas'
    ],
    include_package_data=True,
    entry_points={
        'console_scripts': [
            "debtsum=debtsum.main:main"
        ]
    },
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Build Tools',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8'
    ],
)