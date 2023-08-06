from setuptools import setup

def readme():
    with open('README.md') as f:
        README =f.read()
    return README
    
setup(
    name="instantAPI",
    version="1.0.1",
    description="instant way to create a flask api for your databases",
    long_description=readme(),
    long_description_content_type='text/markdown',
    url='https://github.com/SAVE-POlNT/instantAPI',
    author="Mehdi YAHIA CHERIF",
    licence='GPLv3',
    classifiers=[
    "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
    "Programming Language :: Python :: 3" ,
    "Programming Language :: Python :: 3.7",
    ],
    packages=['instant_API'],
    include_package_data=True,
    install_requires=[],
    entry_points={
    "console_scripts":[
        "instant-API=instant_API.instantAPI:main",
    ]
    }
    )
    
    