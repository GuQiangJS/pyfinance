# Copyright (C) 2018 GuQiangJs.
# Licensed under https://www.gnu.org/licenses/gpl-3.0.html <see LICENSE file>

import unittest
import pandas as pd
import os
import matplotlib.pyplot as plt
from datas import capture,translate
import datetime

class MyTestCase(unittest.TestCase):
    """
    绘图示例
    """

    def __get_symbol_daily_filepath__(self, symbol):
        """
        获取指定股票的每日成交汇总文件路径
        :param symbol:
        :return:
        """
        return os.path.join('testdatas', 'dailies', '{0}.csv'.format(symbol))

    def __read_symbol_daily__(self, symbol, usecols, index_col, parse_dates=True, encoding='utf-8'):
        file = self.__get_symbol_daily_filepath__(symbol)
        if os.path.isfile(file):
            return pd.read_csv(self.__get_symbol_daily_filepath__(symbol), index_col=index_col, usecols=usecols,
                               encoding=encoding, na_values=['nan'], parse_dates=parse_dates)
        return None

    def test_plot_close(self):
        """
        绘制单一股票的收盘价图表
        :return:
        """
        # 创建数据区间
        start_date = '2017-01-01'
        end_date = '2017-02-01'
        dates = pd.date_range(start_date, end_date)
        # 创建一个空的DataFrame
        df1 = pd.DataFrame(index=dates)
        # 读取 csv 文件到临时 DataFrame，只读取其中的 Date 列和 Close 列，索引列为 Date，转换空值为 nan，转换日期字段
        dfs = self.__read_symbol_daily__('000002', ['Date', 'Close'], 'Date')
        self.assertFalse(dfs.empty)
        # 使用 DataFrame.join 方法将两个 DataFrame 连接在一起
        df1 = df1.join(dfs, how='inner')

        df1.plot()
        plt.show()

    def test_plot_mulit_symbol(self):
        """
        读取多只股票放在同一个 DataFrame 中，并绘图
        :return:
        """
        symbols = ['000001', '000002']
        # 创建数据区间
        start_date = '2017-01-01'
        end_date = '2017-02-01'
        dates = pd.date_range(start_date, end_date)
        # 创建一个空的DataFrame
        df1 = pd.DataFrame(index=dates)
        for symbol in symbols:
            # 读取 csv 文件到临时 DataFrame，只读取其中的 Date 列和 Close 列，索引列为 Date，转换空值为 nan，转换日期字段
            dfs = self.__read_symbol_daily__(symbol, ['Date', 'Close'], 'Date')
            self.assertFalse(dfs.empty)

            # 因为多个股票都读取 Close 列，被加入到 df1 时会报错
            # ValueError: columns overlap but no suffix specified: Index(['Close'], dtype='object')
            # 所以需要在加入到 df1 之前对循环中的每个临时表的 Close 列进行重命名，使其唯一
            dfs = dfs.rename(columns={'Close': symbol})

            # 使用 DataFrame.join 方法将两个 DataFrame 连接在一起
            df1 = df1.join(dfs, how='inner')

        df1.plot()
        plt.show()

    def test_fillna(self):
        re=capture().online_daily_sohu('300104',start_date=datetime.date(2017,4,1),end_date=datetime.date(2018,2,28))
        df =  translate.daily_json_to_dataframe(re)
        df1=pd.DataFrame(index=['Date'])
        df['date'] = pd.to_datetime(df['Date'])
        df.set_index("Date", inplace=True)
        df1=df1.join(df)
        print(df)
        df.plot()
        plt.show()


if __name__ == '__main__':
    unittest.main()
