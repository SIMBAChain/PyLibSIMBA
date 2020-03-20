import setuptools

INSTALL_REQUIRES = [
    'web3>=5.1.0',
    'pywallet>=0.1.0',
    'ecdsa>=0.13.3'
]


with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name='PyLibSIMBA',
    version='0.1.7',
    packages=setuptools.find_packages(),
    url='https://simbachain.com/',
    license='License :: OSI Approved :: MIT License',
    author='SIMBA Chain',
    author_email='info@simbachain.com',
    description='A library simplifying the use of SIMBAChain APIs',
    long_description=long_description,
    long_description_content_type="text/markdown",
    install_requires=INSTALL_REQUIRES,
    python_requires='>=3.6',
    setup_requires=['wheel'],
    extras_require={
        'dev': [
            'pytest>=5.1.3',
            'sphinx',
            'sphinx-rtd-theme'
        ]
    },
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Build Tools',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3.6',
    ]
)
