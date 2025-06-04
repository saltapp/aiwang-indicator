**aiwang-indicator** 是一个采用类似通达信指标接口的 Python 技术指标编辑公式库。用户可以像在通达信中一样，使用简洁的TDX style语法进行各类技术指标的编写与回测，非常适合量化研究和策略开发。

> **说明：本项目中的部分代码来自开源项目 [MyTT](https://github.com/mpquant/MyTT)，特此致谢。**

---

## 目录

- [特性](#特性)
- [安装](#安装)
- [快速开始](#快速开始)
- [进阶用法](#进阶用法)
- [贡献与反馈](#贡献与反馈)

---

## 特性

- 通达信风格的指标函数接口，极易上手
- 支持主流金融数据加载（默认采用AkShare）
- 丰富的常用指标函数，支持自定义扩展
- 兼容 numpy/pandas，便于数据分析

---

## 安装

```bash
pip install aiwang-indicator
```

---

## 快速开始

以下是一个简单示例，演示如何使用 **aiwang-indicator** 加载数据并计算指标：

### 1. 数据加载与环境初始化

```python
from aiwang_indicator import set_data_loader
from aiwang_indicator.data.loader.ak_loader import AkLoader

# 初始化数据加载器
data_loader = AkLoader(start_date='20240101')
set_data_loader(data_loader, default_stock_id="600900", default_freq='daily')
```

### 2. 常用行情数据序列变量

#### 默认行情数据序列

| 变量        | 含义         |
|-------------|--------------|
| `CLOSE()`/`C` | 默认收盘价序列 |
| `OPEN()`/`O`  | 默认开盘价序列 |
| `HIGH()`/`H`  | 默认最高价序列 |
| `LOW()`/`L`   | 默认最低价序列 |
| `DATE()`/`D`  | 默认日期序列      |

#### 带参数行情数据序列

| 函数         | 说明                         |
|--------------|------------------------------|
| `CLOSE('代码')` | 获取指定股票的收盘价序列 |
| `OPEN('代码')`  | 获取指定股票的开盘价序列 |
| `HIGH('代码')`  | 获取指定股票的最高价序列 |
| `LOW('代码')`   | 获取指定股票的最低价序列 |
| `DATE('代码')`  | 获取指定股票的日期序列   |
| `CLOSE('周期')` | 获取指定周期的收盘价序列 |
| `OPEN('周期')`  | 获取指定周期的开盘价序列 |
| `HIGH('周期')`  | 获取指定周期的最高价序列 |
| `LOW('周期')`   | 获取指定周期的最低价序列 |
| `DATE('周期')`  | 获取指定周期的日期序列   |
| `CLOSE('代码', '周期')`          | 获取指定股票指定周期的收盘价序列<br>如：`CLOSE('600519', 'weekly')` 获取600519的周线收盘价 |
| `OPEN('代码', '周期')`           | 获取指定股票指定周期的开盘价序列<br>如：`OPEN('600519', 'weekly')` 获取600519的周线开盘价   |
| `HIGH('代码', '周期')`           | 获取指定股票指定周期的最高价序列<br>如：`HIGH('600519', 'weekly')` 获取600519的周线最高价   |
| `LOW('代码', '周期')`            | 获取指定股票指定周期的最低价序列<br>如：`LOW('600519', 'weekly')` 获取600519的周线最低价     |
| `DATE('代码', '周期')`           | 获取指定股票指定周期的日期序列<br>如：`DATE('600519', 'weekly')` 获取600519的周线日期       |


### 3. 指标函数示例

**计算指数化序列**

```python
from aiwang_indicator import *

idx = INDEX(C)  # 将收盘价序列指数化，首日为1000
```

**计算 KDJ 指标**

```python
from aiwang_indicator import *

N = 9
M1 = 3
M2 = 3

RSV = (C - LLV(L, N)) / (HHV(H, N) - LLV(L, N)) * 100
K = SMA(RSV, M1, 1)
D = SMA(K, M2, 1)
J = 3 * K - 2 * D
```

**直接获取数据序列**

```python
from aiwang_indicator import *

close_prices = CLOSE()           # 获取默认股票的收盘价序列
open_prices = OPEN('600519')     # 获取指定股票的开盘价序列
close_prices = CLOSE('600519', 'weekly')        #获取600519的周线收盘价
```

---

## 进阶用法

- 支持自定义数据加载器
- 支持多周期、多标的切换
- 可与 pandas/numpy 等生态无缝结合

---

## 贡献与反馈

欢迎提交 Issue 或 PR，完善指标库与文档！