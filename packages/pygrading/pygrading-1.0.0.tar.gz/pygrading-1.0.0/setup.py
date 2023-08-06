'''
    Name: setup.py
    Author: Charles Zhang <694556046@qq.com>
    Propose: Setup script for pygrading!
    Coding: UTF-8
'''

# 在setup.py的目录下，每次提交记得修改版本号，并删除之前生成的文件
# python setup.py sdist bdist_wheel
# python -m twine upload dist/*

import setuptools

from pygrading import __version__

with open('README.md', 'r') as fh:
    long_description = fh.read()

setuptools.setup(
    name='pygrading',
    version=__version__,
    author='Charles Zhang',
    author_email='694556046@qq.com',
    description='A Python ToolBox for CourseGrading platform.',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://gitlab.educg.net/zhangmingyuan/PyGrading',
    packages=['pygrading'],
    package_data={
        'pygrading': ['static/.gitignore', 'static/*', 'static/kernel/*'],
    },
    classifiers=[
        'Programming Language :: Python :: 3',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.5',
    install_requires=[
        'tqdm>=4.52.0',
        'fire>=0.3.1'
    ],
)
