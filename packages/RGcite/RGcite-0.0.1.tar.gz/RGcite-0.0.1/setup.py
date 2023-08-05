from setuptools import setup, find_packages

classifiers = [
    'Development Status :: 5 - Production/Stable',
    'Intended Audience :: Education',
    'Operating System :: Microsoft :: Windows :: Windows 10',
    'License :: OSI Approved :: MIT License',
    'Programming Language :: Python :: 3'
]

setup(
    name='RGcite',
    version='0.0.1',
    description='A web scraping function to find citations, link to articles and titles of articles of a particular '
                'author ',
    long_description=open('README.txt').read() + '\n\n' + open('CHANGELOG.txt').read(),
    url='',
    author='Rajat Puri',
    author_email='purirajat.rp@gmail.com',
    license='MIT',
    classifiers=classifiers,
    keywords='Citations, Research gate',
    packages=find_packages(),
    install_requires=['']
)
