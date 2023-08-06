from setuptools import setup, find_packages

#python3 setup.py build
#python3 setup.py sdist


VERSION = "0.0.6"

setup(
    name="PyXtSoaWebservice",
    version=VERSION,
    author="Alexandre Defendi",
    author_email='alexandre_defendi@hotmail.com',
    description='PyXtSoaWebservice é uma biblioteca de acesso a API da Serasa, utilizando o distribuidor autorizado SOA Webservices',
    long_description=open('README.md', 'r').read(),
    long_description_content_type="text/markdown",

    keywords=['serasa','consulta','CPF','CNPJ'],
    classifiers=[
        'Environment :: Plugins',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: GNU Lesser General Public License v2 or later (LGPLv2+)',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.4',
        'Topic :: Software Development :: Libraries :: Python Modules',
    ],
    python_requires='>=3.4',
    packages=find_packages(exclude=['*test*']),
    package_data={
        'pyxtsoawebservice': []
    },
    url='https://bitbucket.org/defendi/pyxtsoawebservice',
    license='LGPL-v2.1+',
    install_requires=[
        'lxml >= 3.5.0, < 5',
        'zeep',
    ],
    tests_require=[
        'pytest',
    ],
)