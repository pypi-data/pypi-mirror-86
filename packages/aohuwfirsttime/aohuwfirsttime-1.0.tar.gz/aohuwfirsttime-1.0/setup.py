from distutils.core import setup

setup(
    name="aohuwfirsttime",  #对外我的模块的名字
    version="1.0", #版本号
    description="这是一个对外发布模块的测试",
    author="Huw",
    author_email="howlland@126.com",
    py_modules=["baizhanSuperMath.demo01","baizhanSuperMath.demo02"]  #要发布的模块
)