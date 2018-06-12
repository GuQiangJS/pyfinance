## 第六章 金融时间序列

### 6.1 pandas基础

* [pandas](http://pandas.pydata.org/pandas-docs/stable/api.html#id7)

* [DataFrame](http://pandas.pydata.org/pandas-docs/stable/api.html#dataframe)

* [pandas.date_range](http://pandas.pydata.org/pandas-docs/stable/generated/pandas.date_range.html#pandas-date-range)

* [pandas.DataFrame.plot](http://pandas.pydata.org/pandas-docs/stable/generated/pandas.DataFrame.plot.html)

* [pandas.Series.plot](http://pandas.pydata.org/pandas-docs/stable/generated/pandas.Series.plot.html#pandas.Series.plot)

* [pandas.Series](http://pandas.pydata.org/pandas-docs/stable/generated/pandas.Series.html#pandas.Series)

* [groupby](http://pandas.pydata.org/pandas-docs/stable/search.html?q=groupby&check_keywords=yes&area=default)

### 6.2 金融数据

[pandas-datareader](http://pandas-datareader.readthedocs.io/en/latest/)

* [波动性](https://zh.wikipedia.org/wiki/%E6%B3%A2%E5%8A%A8%E6%80%A7)

波动率对期权交易者特别重要，而（技术型）股票交易者可能对移动平均值（所谓趋势）更感兴趣。

移动平均值很容易用 [pandas.rolling_mean](http://pandas.pydata.org/pandas-docs/version/0.17.0/generated/pandas.rolling_mean.html) -> [pandas.DataFrame.rolling](https://pandas.pydata.org/pandas-docs/stable/generated/pandas.DataFrame.rolling.html) 计算。

> [What’s New v0.23.0 (May 15, 2018)](https://pandas.pydata.org/pandas-docs/stable/whatsnew.html?highlight=rolling_mean)

### 6.3 回归分析

[pandas.read_csv](http://pandas.pydata.org/pandas-docs/stable/generated/pandas.read_csv.html?highlight=read_csv#pandas.read_csv)

### 6.4 高频数据 - 分时数据

## 第七章 输入/输出操作

### Python基本I/O

#### 读写对象

[pickle — Python object serialization](https://docs.python.org/3/library/pickle.html)

为确保读写后的对象相同， `Numpy` 提供了 [allclose](https://www.numpy.org/devdocs/reference/generated/numpy.allclose.html?highlight=allclose#numpy.allclose) 函数。原理上使用 `np.sum(np.array(a) - np.array(b))`，检查是否为0的效果一样。

```python
import pickle

# 将多个对象按照字典的方式写入
pkl_file=open('data.pkl','w')
pickle.dump({'x':x,'y':y},pkl_file)
pkl_file.close()

# 读取
pkl_file=open('data.pkl','r')
data=pickle.load(pkl_file)
pkl_file.close()
for key in data.keys():
    pass
```

#### 从 SQL 到 pandas

[pandas.read_sql](http://pandas.pydata.org/pandas-docs/stable/generated/pandas.read_sql.html?highlight=io%20sql#pandas.read_sql)

[HDF文件格式 - wikipedia](https://zh.wikipedia.org/wiki/HDF)

> HDF（英语：Hierarchical Data Format）指一种为存储和处理大容量科学数据设计的文件格式及相应库文件。

[HDFStore: PyTables (HDF5)](http://pandas.pydata.org/pandas-docs/stable/api.html#hdfstore-pytables-hdf5)

[PyTables](https://www.pytables.org/index.html)

[HDF5 (PyTables)](http://pandas.pydata.org/pandas-docs/stable/io.html?highlight=pytables#hdf5-pytables)

> `PyTables` 是 `python` 与 HDF5 数据库/文件标准的结合。它专门为优化I/O操作的性能、最大限度的利用可用硬件而设计。
>
> 使用 `PyTables` 的主要优势之一是压缩方法。 [pandas.DataFrame.to_hdf](http://pandas.pydata.org/pandas-docs/stable/generated/pandas.DataFrame.to_hdf.html?highlight=pytables)

#### 内存外计算

[The EArray class](https://www.pytables.org/usersguide/libref/homogenous_storage.html#tables.EArray)

[Expr](https://www.pytables.org/usersguide/libref/expr_class.html?highlight=expr#tables.Expr) 模块用于高效的处理数值表达式。

```
>>> a = f.create_array('/', 'a', np.array([1,2,3]))
>>> b = f.create_array('/', 'b', np.array([3,4,5]))
>>> c = np.array([4,5,6])
>>> expr = tb.Expr("2 * a + b * c")   # initialize the expression
>>> expr.eval()                 # evaluate it
array([14, 24, 36])
>>> sum(expr)                   # use as an iterator
74
```

## 第八章 高性能Python

* [numexpr](https://github.com/pydata/numexpr) [numexpr document](http://numexpr.readthedocs.io/en/latest/)

```
>>> import numpy as np
>>> import numexpr as ne

>>> a = np.arange(1e6)   # Choose large arrays for better speedups
>>> b = np.arange(1e6)

>>> ne.evaluate("a + 1")   # a simple expression
array([  1.00000000e+00,   2.00000000e+00,   3.00000000e+00, ...,
         9.99998000e+05,   9.99999000e+05,   1.00000000e+06])

>>> ne.evaluate('a*b-4.1*a > 2.5*b')   # a more complex one
array([False, False, False, ...,  True,  True,  True], dtype=bool)

>>> ne.evaluate("sin(a) + arcsinh(a/b)")   # you can also use functions
array([        NaN,  1.72284457,  1.79067101, ...,  1.09567006,
        0.17523598, -0.09597844])

>>> s = np.array(['abba', 'abbb', 'abbcdef'])
>>> ne.evaluate("'abba' == s")   # string arrays are supported too
array([ True, False, False], dtype=bool)
```

### 并行计算

[Using IPython for parallel computing](https://ipython.org/ipython-doc/3/parallel/)

```python
import numpy as np
from IPython.parallel import Client
# default配置文件保存群集配置。该文件保存了 IPython.parallel 需要哪个集群用于代码并行执行的相关信息。
c=Client(profile='default')
# 在群集上生成一个视图
view=c.load_balanced_view()

def bsm_mcs_valuation(strike):
    """
    单线程估值算法
    """
    pass

def par_value(n):
    strikes=np.linspace(80,120,n)
    option_values=[]
    for strike in strikes:
        # 估值函数通过 view.apply_async 异步应用到群集视图，这实际上一次性初始化所有并行估值。
        value=view.apply_async(bsm_mcs_valuation,strike)
        option_values.append(value)
    c.wait(option_values)
    return strikes,option_values

# 结果包含在对象的 result 属性中
# option_values[0].result
```

### 多处理

[multiprocessing — Process-based parallelism](https://docs.python.org/3.8/library/multiprocessing.html)

### 动态编译

[Numba](https://numba.pydata.org/)

