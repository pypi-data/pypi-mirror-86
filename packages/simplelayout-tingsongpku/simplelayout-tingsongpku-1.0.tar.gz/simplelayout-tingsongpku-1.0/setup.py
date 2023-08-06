#!/usr/bin/env python
# coding=utf-8

from setuptools import setup, find_packages


setup(
    name="simplelayout-tingsongpku",  # pypi中的名称，pip或者easy_install安装时使用的名称
    version="1.0",
    author="tingsong",  # 描述性文字，可选
    author_email="tingsong@pku.edu.cn",  # 描述性文字，可选
    description=("This is a simplelayout package"),  # 描述性文字，可选
    license="GPLv3",  # 描述性文字，可选
    keywords="simple layout",  # 描述性文字，可选
    url="https://ssl.xxx.org/redmine/projects/RedisRun",  # 描述性文字，可选
    # packages=find_packages(),
    # 需要打包的目录列表,需包含src/simplelayout，需指定src目录？？
    package_dir={'': 'src'},
    packages=find_packages(where="src"),  # Required
    # 需要安装的依赖包，有些是自己编写的或者网上的
    install_requires=[
        'setuptools>=16.0',
        'pytest',
        'numpy',
        'matplotlib',
        'scipy'
    ],

    # 添加这个选项，在windows下Python目录的scripts下生成exe文件
    # 注意：模块与函数之间是冒号:
    # 设置了在命令行中如何使用 XX_module 中的 main 函数，直接命令行调用
    entry_points={'console_scripts': [
        'simplelayout = simplelayout.__main__:main',
    ]},

    # long_description=read('README.md'),
    classifiers=[  # 程序的所属分类列表，描述性文字，可选
        "Development Status :: 3 - Alpha",
        "Topic :: Utilities",
        "License :: OSI Approved :: GNU General Public License (GPL)",
    ],
    # 此项需要，否则卸载时报windows error
    zip_safe=False
)
