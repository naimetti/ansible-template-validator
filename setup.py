from setuptools import setup

with open('README.md') as readme_file:
    readme = readme_file.read()

setup(
    name="ansible_template_validator",
    version='0.1.4',
    author="Nicolas Aimetti",
    author_email="naimetti@yahoo.com.ar",
    description="A helper script to use with the validate option from ansible template module",
    long_description=readme,
    long_description_content_type="text/markdown",
    url='https://github.com/naimetti/ansible-template-validator',
    python_requires='>=2.7, !=3.0.*, !=3.1.*, !=3.2.*, !=3.3.*',
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'Intended Audience :: System Administrators',
        'License :: OSI Approved :: MIT License',
        'Natural Language :: English',
        "Programming Language :: Python :: 2",
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Topic :: System :: Installation/Setup',
        'Topic :: System :: Systems Administration',
    ],
    py_modules=['ansible_template_validator'],
    install_requires=[],
    test_suite='tests',
    entry_points={
        'console_scripts': ['ansible-template-validator=ansible_template_validator:main'],
    }
)
