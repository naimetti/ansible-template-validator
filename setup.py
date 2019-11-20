
from setuptools import setup

setup(
    name="ansible-template-validator",
    version="0.1.0",
    author="Nicolas Aimetti",
    author_email="naimetti@yahoo.com.ar",
    description="A lib for validate configs to use with ansible",
    py_modules='ansible_template_validator',
    install_requires=[],
    test_suite='tests',
    entry_points={
        'console_scripts': ['ansible-template-validator=ansible_template_validator:main'],
    },
)
