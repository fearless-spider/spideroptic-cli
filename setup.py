
from setuptools import setup, find_packages
from spideroptic.core.version import get_version

VERSION = get_version()

f = open('README.md', 'r')
LONG_DESCRIPTION = f.read()
f.close()

setup(
    name='spideroptic',
    version=VERSION,
    description='Spider Optic forex guider',
    long_description=LONG_DESCRIPTION,
    long_description_content_type='text/markdown',
    author='Przemyslaw Pajak FEARLESS SPIDER',
    author_email='office@fearlessspider.com',
    url='http://spideroptic.pl/',
    license='MIT',
    packages=find_packages(exclude=['ez_setup', 'tests*']),
    package_data={'spideroptic': ['templates/*']},
    include_package_data=True,
    entry_points="""
        [console_scripts]
        spideroptic = spideroptic.main:main
    """,
)
