from setuptools import setup

setup(
    name='nug-dongle',
    version='0.1.0',
    packages=['nug_dongle'],
    url='https://github.com/Sibyx/nug-dongle',
    license='GPLv3',
    author='Jakub Dubec',
    author_email='jakub.dubec@gmail.com',
    description='Dongle service in the Nug Project',
    entry_points={
        'console_scripts': [
            "nug-dongle = nug_dongle.__main__:main",
        ]
    },
    install_requires=[
        'python-dotenv==0.20.*',
        'zeroconf==0.38.*',
        'tomli >= 1.1.0 ; python_version < "3.11"',
    ],
)
