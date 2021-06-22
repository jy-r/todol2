import sys
import setuptools


install_requires = [
    'colorama',
    'prompt_toolkit'
]

setuptools.setup(
    name='todol',
    version='2',
    description='A simple terminal To-do list manager',
    long_description='A simple terminal To-do list manager',
    long_description_content_type='text/markdown',
    url='https://github.com/jy-r/todol2',
    author='jy-r',
    author_email='',
    license='MIT',
    keywords='to-do manager, productivity tools',
    packages=[
        'todol'
    ],
    package_data={
    },
    install_requires=install_requires,
    entry_points={'console_scripts': ['todol=todol.todol:main']},
    classifiers=[
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Topic :: Terminals',
        ],
)
