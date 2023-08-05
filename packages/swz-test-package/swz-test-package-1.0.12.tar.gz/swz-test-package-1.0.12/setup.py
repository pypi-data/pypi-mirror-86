from setuptools import setup, find_packages

VERSION = __import__('test_package').__version__

setup(
    name='swz-test-package',
    version=VERSION,
    author='swz',
    license='Apache License 2.0',
    # scripts=['test_package/bin/cmdt.py'],
    platforms='any',
    packages=find_packages(exclude=['tests*']),
    package_data={
        '': ['*']
    },
    entry_points="""
    [console_scripts]
    cmdt=test_package.bin.cmdt:run
    """
)
