"""
Neufbox API Client
"""
from setuptools import setup, find_packages


with open('README.md', 'r') as readme_file:
    LONG_DESCRIPTION = readme_file.read()


setup(
    name='neufbox-client',
    description='Neufbox API Client',
    author='Sylvain Prat',
    author_email='sylvain.prat+neufbox-client@gmail.com',
    long_description=LONG_DESCRIPTION,
    long_description_content_type="text/markdown",
    license='MIT License',
    keywords='neuf, sfr, redbysfr, box, api, client',
    url='https://github.com/sprat/neufbox-client',
    download_url='https://pypi.python.org/pypi/neufbox-client',
    use_scm_version=True,
    setup_requires=[
        'setuptools_scm',
    ],
    install_requires=[
        'requests',
        'xmltodict'
    ],
    packages=find_packages(),
    extras_require={
        'test': [
            'python-dotenv',
            'pytest',
            'pytest-cov',
            'pytest-pylint',
            'requests-mock'
        ],
    },
    python_requires='>=3.6',
    platforms='any',
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Developers',
        'Intended Audience :: Information Technology',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 3 :: Only',
        'Topic :: System :: Networking',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'Topic :: Software Development :: Libraries :: Application Frameworks',
    ],
)
