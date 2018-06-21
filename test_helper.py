# Copyright (C) 2018 GuQiangJs.
# Licensed under https://www.gnu.org/licenses/gpl-3.0.html <see LICENSE file>

import datetime
import os
import unittest

import matplotlib.pyplot as plt
import pandas as pd
from matplotlib.font_manager import FontProperties

from datas import capture


class MyTestBase(unittest.TestCase):

    def setUp(self):
        """
        当数据不存在时，自动在testdatas目录下的dailies目录中增加 000001,000002,300001,300002,600001,600003,上证指数(zs_000001),深证成指(zs_399001) 的每日成交汇总csv文件

        获取 2004-10-08 ~ 2017——12-31 之间的数据

        处理顺序：

        1. 使用 `datas.capture.online_daily_sohu` 方法获取指定数据。

        2. 使用 `pandas.DataFrame` 构建数据表，并将数据表保存。
        :return:
        """
        TEST_FOLDER = os.path.join('testdatas', 'dailies')
        END_DATE = datetime.date(2017, 12, 31)

        if not os.path.exists(TEST_FOLDER):
            os.makedirs(TEST_FOLDER, exist_ok=True)

        symbols = ['zs_000001', 'zs_399001', '000001', '000002', '300001', '300002', '600001', '600003']
        c = capture()
        for symbol in symbols:
            filename = get_symbol_daily_filepath(symbol)
            if not os.path.isfile(filename):
                re = c.online_daily_sohu(symbol, prefix=('' if len(symbol) > 6 else 'cn_'), end_date=END_DATE)
                # 使用二维数组构建 `pands.DataFrame` ，并按照顺序指定列头
                pdd = pd.DataFrame(re[0]['hq'],
                                   columns=['Date', 'Open', 'Close', 'Change', 'Quote', 'Low', 'High', 'Volume',
                                            'Turnover', 'Rate'])
                # 保存 `pandas.DataFrame` 至 `csv` 格式。跳过索引列
                pdd.to_csv(filename, mode='w+', encoding='utf-8', index=False)


# 设置matplotlib可用中文字体
ZH_FONT_NOTO_SANS = FontProperties(fname=os.path.join('fonts', 'NotoSansCJKsc-Medium.otf'))


def get_symbol_daily_filepath(symbol):
    """
    获取指定股票的每日成交汇总文件路径
    :param symbol: 股票代码
    Examples: 0000002,szzs(上证指数)
    :return:
    """
    return os.path.join('testdatas', 'dailies', '{0}.csv'.format(symbol))


def read_symbol_daily(symbol, usecols, index_col: [], parse_dates=True, encoding='utf-8'):
    """
    根据指定股票代码读取每日成交汇总数据
    Args:
        self:
        symbol:
        usecols:
        index_col:
        parse_dates:
        encoding:

    Returns:

    """
    file = get_symbol_daily_filepath(symbol)
    if os.path.isfile(file):
        return pd.read_csv(file, index_col=index_col, usecols=usecols,
                           encoding=encoding, na_values=['nan'], parse_dates=parse_dates)
    return None


def read_symbol_daily_close(symbols: [], parse_dates=True, encoding='utf-8', start_date: str = None,
                            end_date: str = None, drop_na_in_first: bool = True, fill_nan_f: bool = True,
                            fill_nan_b: bool = True):
    """
    读取多支股票的 `Close` 数据，并合并为一个 dataframe。使用 `Date` 字段作为索引。

    **会使用 `symbols` 中的第一个作为主表，其后的其他数据中的 `Close` 数据，采用 `on=left` 的方式与主表关联。**
    Args:
        fill_nan_f: 除第一个 symbol 外的 `Close` 列数据，遇到 NaN 值是，是否向前填充。
        fill_nan_b: 除第一个 symbol 外的 `Close` 列数据，遇到 NaN 值是，是否向后填充。
        drop_na_in_first: 当第一个 symbol 中的 `Close` 列包含 NaN 值时，是否丢弃该行数据。
        symbols:
        symbol:
        index_col:
        parse_dates:
        encoding:
        start_date: 取值起始日期。Example:2017-01-01
        end_date: 取值结束日期。Example:2019-01-01

    Returns:

    """
    if start_date and end_date:
        dates = pd.date_range(start_date, end_date)
        # 创建一个空的DataFrame
        result = pd.DataFrame(index=dates)
    else:
        result = pd.DataFrame()
    for symbol in symbols:
        pdd = read_symbol_daily(symbol, ['Date', 'Close'], index_col='Date', parse_dates=parse_dates, encoding=encoding)
        pdd = pdd.rename(columns={'Close': symbol})
        result = result.join(pdd)
        if symbols.index(symbol) == 0 and drop_na_in_first:
            result = result.dropna()
        if symbols.index(symbol) > 0:
            if fill_nan_f:
                result = result.fillna(method='ffill')
            if fill_nan_b:
                result = result.fillna(method='bfill')
    return result


def normalize_data(df):
    """
    数据归一化
    Args:
        df:

    Returns:

    """
    return df / df.iloc[0]


def compute_daily_returns(df):
    """
    计算日收益率
    Args:
        df:

    Returns:

    """
    daily_returns = df.copy()
    daily_returns[1:] = (df[1:] / df[:-1].values) - 1
    daily_returns.iloc[0] = 0
    return daily_returns


def plot_data(df, title='', ylabel='', xlabel=''):
    """
    绘图
    Args:
        df:
        title:
        ylabel:

    Returns:

    """
    df.plot()
    if title:
        plt.title(title, fontproperties=ZH_FONT_NOTO_SANS)
    if ylabel:
        plt.ylabel(ylabel, fontproperties=ZH_FONT_NOTO_SANS)
    if xlabel:
        plt.xlabel(xlabel, fontproperties=ZH_FONT_NOTO_SANS)
    plt.show()
