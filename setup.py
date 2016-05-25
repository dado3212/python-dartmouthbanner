from setuptools import setup

long_description="""This API allows Python programs to easily interact with Dartmouth Banner."""

setup(
    name='python-dartmouthbanner',
    version='1.1',
    description='Python API for interacting with Dartmouth Banner',
    url='https://github.com/dado3212/python-dartmouthbanner',
    author='Alex Beals',
    author_email='Alex.Beals.18@dartmouth.edu',
    license='BSD',
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3'
    ],
    keywords='api dartmouth banner',
    packages=['dartmouthbanner'],
    long_description=long_description,
    install_requires=['requests', 'urllib', 'shutil', 'Pillow']
)
