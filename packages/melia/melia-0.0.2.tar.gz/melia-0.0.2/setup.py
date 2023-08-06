import pathlib
from setuptools import setup

HERE = pathlib.Path(__file__).parent

README = (HERE/'README.md').read_text()

setup(
    name='melia',
    version='0.0.2',
    description='Meta-linguistic abstractions',
    long_description=README,
    long_description_content_type='text/markdown',
    author='dindefi',
    author_email='dindefi@gmail.com',
    licence='Apache 2.0',
    include_package_data=True,
    pacakge_dir={'melia': 'src'},
    pacakages=['melia'],
    entry_points={
        'console_scripts': [
            'melia=melia.main:start',
        ]  
    }
)


