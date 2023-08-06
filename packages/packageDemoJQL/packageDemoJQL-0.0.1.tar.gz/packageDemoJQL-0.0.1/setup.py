import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="packageDemoJQL", # 包版本名称，必须唯一(不能和你在pypi.org上已有的包重名)
    version="0.0.1",
    author="jianqiangli",  #确认包的作者
    author_email="861865739@qq.com",  #确认包的作者
    description="A small example package", #包的简短描述
    long_description=long_description,     #包的详细描述，通常写在readme.md文件中然后载入
    long_description_content_type="text/markdown", #包的详细描述的文件的类型
    url="https://github.com/pypa/sampleproject",   #包的工程主页地址
    packages=setuptools.find_packages(),           #版本软件包中应包括的所有Python导入软件包的列表，本例为packageTest，可以用find_packages()自动找到所有的包和子包
    classifiers=[    #至少包含一下三项
        "Programming Language :: Python :: 3",     #包的语言及语言版本
        "License :: OSI Approved :: MIT License",  #包在哪个证书下有效
        "Operating System :: OS Independent",      #包运行的操作系统
    ],
    python_requires='>=3.6',
)