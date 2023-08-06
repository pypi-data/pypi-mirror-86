from setuptools import setup, find_packages
from setuptools.command.install import install
import sys
import os


# class PostInstallCommand(install):
#     def run(self):
#         # 这里加入我们要执行的代码
#         print("------------------------------------------------")
#         if os.name == "posix":
#             os.system("/Applications/海龟编辑器.app/Contents/Resources/app/python/bin/python3 -m pip install -i http://mirrors.aliyun.com/pypi/simple/ --trusted-host mirrors.aliyun.com argon2-cffi==19.2.0")
#             os.system("/Applications/海龟编辑器.app/Contents/Resources/app/python/bin/python3 -m pip install -i http://mirrors.aliyun.com/pypi/simple/ --trusted-host mirrors.aliyun.com vpython")

#         install.run(self)


setup(

    name="goodstar",

    version="0.0.1",

    author="seale",

    author_email="seale@outlook.com",

    description="A Python library for test.",

    license="MIT",

    packages=find_packages(),
    package_data={"": ["*.so", "*.pyd"], "goodstar": ["demo/*.py"]},
    # install_requires=["vpython"],
    # cmdclass={
    #     'install': PostInstallCommand,
    # }

)
