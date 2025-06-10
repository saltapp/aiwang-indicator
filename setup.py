import codecs
import os
from setuptools import setup, find_packages

# these things are needed for the README.md show on pypi
here = os.path.abspath(os.path.dirname(__file__))

with codecs.open(os.path.join(here, "README.md"), encoding="utf-8") as fh:
    long_description = "\n" + fh.read()


VERSION = '0.1.5'
DESCRIPTION = 'aiwang-indicator 是一个采用通达信指标接口的 Python 技术指标编辑公式库。用户可以像在通达信中一样,使用简洁的TDX style语法进行各类技术指标的编写与回测,非常适合量化研究和策略开发。'

# Setting up
setup(
    name="aiwang-indicator",
    version=VERSION,
    author="aiwangwang",
    description=DESCRIPTION,
    long_description_content_type="text/markdown",
    long_description=long_description,
    packages=find_packages(),
    install_requires=[
        "numpy",
        "pandas",
        "akshare",
    ],
    keywords=["通达信指标", 'TDX', "技术指标", "量化"],
)