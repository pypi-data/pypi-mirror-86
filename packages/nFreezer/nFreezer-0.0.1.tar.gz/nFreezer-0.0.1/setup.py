from setuptools import setup

setup(
    name='nFreezer',
    version='0.0.1',
    author="Joseph Ernest",
    author_email="nouvellecollection@gmail.com",
    description="nFreezer is an encrypted-at-rest backup tool over SFTP.",
    # long_description=freezer.__doc__.split('==')[0].strip(),
    long_description=open('README.md').read(),
    long_description_content_type="text/markdown",
    url="https://github.com/josephernest/nfreezer",
    platforms='any',
    license='MIT with free-of-charge-redistribution clause',
    classifiers=[
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
    ],
    py_modules=['nfreezer'],
    install_requires=['pysftp', 'pycryptodome'],
    python_requires='>=3.6',        
    entry_points='''
        [console_scripts]
        nfreezer=nfreezer:console_script
    '''
)