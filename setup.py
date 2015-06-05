from setuptools import setup, find_packages

setup(
    name='dartmouth_banner',

    version='1.0.0',

    description='Python API for interacting with Dartmouth Banner',

    url='https://github.com/dado3212/dartmouth_banner',

    author='Alex Beals',
    author_email='Alex.Beals.18@dartmouth.edu',

    license='BSD',

    classifiers=[
        'Development Status :: 3 - Alpha',

        'Intended Audience :: Developers',

        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.2',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
    ],

    keywords='api dartmouth banner',

    packages=find_packages(),

    install_requires=['requests','re']
)