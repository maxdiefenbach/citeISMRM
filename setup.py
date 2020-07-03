from setuptools import setup


setup(
    name='citeISMRM',
    version='0.1',
    packages=['citeISMRM'],
    install_requires=['beautifulsoup4', 'bibtexparser'],
    entry_points={
        'console_scripts': ['citeISMRM = citeISMRM.citeISMRM:main']
    }
)

