[![Work in Repl.it](https://classroom.github.com/assets/work-in-replit-14baed9a392b3a25080506f3b7b6d57f295ec2978f6f33ec97e36a161684cbe9.svg)](https://classroom.github.com/online_ide?assignment_repo_id=3702592&assignment_repo_type=AssignmentRepo)
# 3-simplelayout-package

## 简介

- 本次作业将大家完成的数据生成器进行打包，可供 pip 进行安装，发布到 [PyPI](https://pypi.org/)。同时使用 Sphinx 构建文档，发布到 [Read the Docs](https://readthedocs.org/)。


>**Sphinx** is a powerful documentation generator that has many great features for writing technical documentation including:
>- Generate web pages, printable PDFs, documents for e-readers (ePub), and more all from the same sources
>- You can use reStructuredText or Markdown to write documentation
>- An extensive system of cross-referencing code and documentation
>- Syntax highlighted code samples
>- A vibrant ecosystem of first and third-party extensions

- Python 生态的文档大都以 Sphinx 进行发布，例如 [Python 自身的官方文档](https://docs.python.org/3/)、[Pytorch 文档](https://pytorch.org/docs/stable/index.html) 等等。

- [Read the Docs](https://readthedocs.org/) 是一个可以自动化托管 Sphinx 文档的网站。

- Read the Docs 有上手教程，[参考](https://docs.readthedocs.io/en/stable/intro/getting-started-with-sphinx.html)。

## 要求

- 将个人完成的 `2-simplelayout-generator` 项目中的 `simplelayout` 目录复制到本次作业的 `src` 目录下。
- 编写 `setup.py`
  - 参考[官方文档](https://docs.python.org/3/distributing/index.html#reading-the-python-packaging-user-guide)，与 [Packaging and distributing projects](https://packaging.python.org/guides/distributing-packages-using-setuptools/)，正确配置 `setuptools.setup()`，确保能被 `pip` 正确安装，要求
    - package 名称设置为 `simplelayout-github账号名`
    - 正确包含 `src/simplelayout` 这个 package
    - `install_requires` 包含 `simplelayout` 的相关依赖
    - 正确配置 `entry_points`，使命令 `simplelayout` 对应 `simplelayout/__main__.py` 中的 `main()` 函数
- 参考 [文档](https://packaging.python.org/guides/distributing-packages-using-setuptools/#packaging-your-project)，正确打包
- 参考 [文档](https://packaging.python.org/guides/distributing-packages-using-setuptools/#id77)，正确上传到 PyPI
- 根据[参考教程](https://docs.readthedocs.io/en/stable/intro/getting-started-with-sphinx.html)，创建 `docs` 目录，并创建 `Sphinx` 项目。
  - 在执行 `sphinx-quickstart` 时输入相关信息
  - Sphinx 默认使用 rst 格式（[reStructuredText](https://www.sphinx-doc.org/en/master/usage/restructuredtext/basics.html) ）编写文档，可进行配置使用 [Markdown](https://docs.readthedocs.io/en/stable/intro/getting-started-with-sphinx.html#using-markdown-with-sphinx) 进行文档编写。
  - 选做：[参考](https://www.sphinx-doc.org/en/master/usage/extensions/napoleon.html) 配置 autodoc、napoleon 插件，自动生成 simplelayout 中的 docstring API。
  - 在本地生成正确的 Sphinx 文档
- 注册 [Read the Docs](https://readthedocs.org/)，将个人仓库中的文档正确托管
- 将个人项目 PyPI 仓库的链接、read the docs 链接以评论的方式发在 `Feedback` 上

## 注意

本次作业的在线测试分为以下部分：
1. 测试能否正确执行
  ```
  pip install .
  ```
  分值：1 分
1. 测试能否正确执行
  ```
  pip install .
  simplelayout -h
  ```
  分值：1 分

以上测试通过后，会在 `Feedback` 中打印相关信息（包括 PyPI 链接，生成图片），但不会对 `PyPI`、`Read the Docs` 自动测试

## 一些思考笔记：
https://www.cnblogs.com/maociping/p/6633948.html
https://www.jianshu.com/p/9a5e7c935273

1. 在安装python的相关模块和库时，我们一般使用```pip install  模块名```或者```python setup.py install```，前者是在线安装，会安装该包的相关依赖包；后者是下载源码包然后在本地安装，不会安装该包的相关依赖包。一般安装普通包，pip install XXX简单够用；但是，在编写系统时，想要把相关依赖包（有些是自己写的模块，在线找不到，又或者目标机器无法联网）一起打包发布，就需要使用setup.py方式了，只需在 setup.py 文件中写明**依赖的库和版本**，然后到目标机器上使用python setup.py install安装

2. 关于setup.py()的find_package参数：
https://www.cnblogs.com/potato-chip/p/9106225.html
--package_dir 告诉setuptools哪些目录下的文件被映射到哪个源码包。一个例子：package_dir = {'': 'lib'}，表示“root package”中的模块都在lib 目录中。
--find_packages() 对于简单工程来说，手动增加packages参数很容易，刚刚我们用到了这个函数，它默认在和setup.py同一目录下搜索各个含有 init.py的包。
其实我们可以**将包统一放在一个src目录中**，另外，这个包内可能还有aaa.txt文件和data数据文件夹。另外，也可以排除一些特定的包
find_packages(exclude=[".tests", ".tests.", "tests.", "tests"])
--install_requires = ["requests"] 需要安装的依赖包
--entry_points 动态发现服务和插件

个人对使用packages相关参数的看法，
首先告诉程序去哪个目录中找包，因此有了packages参数，
其次，告诉程序我包的起始路径是怎么样的，因此有了package_dir参数
最后，找到包以后，我应该把哪些文件打到包里面，因此有了package_data参数
```
setup(
name = "demo",
version = "0.1",
# 包含所有src目录下的包 ---------项目中的所有源码和测试用例文件目录一般都存放在统一的src目录下方便管理，默认也是创建src目录
packages = find_packages('src'),
package_dir = {'':'src'},
package_data = {
# 包含所有.txt文件
'':['.txt'],
# 包含data目录下所有的.dat文件
'test':['data/.dat'],
}
)
```