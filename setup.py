from setuptools import setup

setup(
    name='denonavr',
    version='1.0.0',
    description='Communicate with an Denon AVR X1000 via telnet over a network.',
    url='https://github.com/toebsen/python-denonavr',
    license='MIT',
    author='toebsen',
    author_email='toebsen@hotmail.com',
    packages=['denonavr'],
    install_requires=['Flask>=0.10.1'],    
    entry_points={
        'console_scripts': [
            'denonavr_server = denonavr.__main__:main'
        ]
    },
    classifiers=[
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 3',
    ]
)