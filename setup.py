from setuptools import setup, find_packages

github = 'https://github.com/jmwri/runehistory-api'
version = '0.0.1'

setup(
    name='runehistory-api',
    packages=find_packages(),
    version=version,
    license='MIT',
    python_requires='>=3.6, <4',
    description='RuneHistory api',
    author='Jim Wright',
    author_email='jmwri93@gmail.com',
    url=github,
    download_url='{github}/archive/{version}.tar.gz'.format(
        github=github, version=version
    ),
    keywords=['runehistory'],
    classifiers=[
        # How mature is this project? Common values are
        #   3 - Alpha
        #   4 - Beta
        #   5 - Production/Stable
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'Topic :: Software Development',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3.6',
    ],
    install_requires=[
        'cmdbus>=1.0.1,<2',
        'evntbus>=1.2.1,<2',
        'ioccontainer>=1.0.5,<2',
        'typing',
        'Flask==0.12.2',
        'pymongo==3.6.0',
        'python-dateutil>=2.6.1,<3',
        'python-slugify==1.2.4',
    ],
    extras_require={
        'test': ['coverage', 'pytest', 'pytest-watch', 'tox']
    },
)
