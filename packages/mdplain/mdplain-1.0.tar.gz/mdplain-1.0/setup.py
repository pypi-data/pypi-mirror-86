from setuptools import setup, find_packages

setup(
    name='mdplain',
    version=1.0,
    description=(
        'convert markdown to plain text'
    ),
    long_description=open('README.rst').read(),
    author='caijunyi',
    author_email='caijunyi08@outlook.com',
    license='MIT License',
    packages=find_packages(),
    url='https://github.com/icaijy/mdplain',
    classifiers=[
        'Programming Language :: Python :: 3',
    ],
    install_requires=[
        'beautifulsoup4',
        'markdown'
    ]
)
