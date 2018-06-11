# Copyright (C) 2018 GuQiangJs.
# Licensed under https://www.gnu.org/licenses/gpl-3.0.html <see LICENSE file>

import datetime
import os
import unittest

import matplotlib.pyplot as plt
import pandas as pd

from datas import capture, translate


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
        # 读取乐视的数据
        leesee = capture().online_daily_sohu('300104', start_date=datetime.date(2017, 4, 1),
                                             end_date=datetime.date(2018, 1, 29))
        df_lee = translate.daily_json_to_dataframe(leesee)
        # 只取Close列的数据，返回值包含索引列+Close列
        df_lee = df_lee[['Close']]
        # 数据中的Close列进行重命名。否则后面Join时，由于两个表都包含Close列，会报错
        df_lee = df_lee.rename(columns={'Close': '300104'})
        print(df_lee)

        # 读取上证指数数据。只要市场运行，上证指数就会有数据。所以读取此数据可知每日是否开市
        shzs = capture().online_daily_sohu_shzs(start_date=datetime.date(2017, 3, 1),
                                                end_date=datetime.date(2018, 2, 28))
        df_shzs = translate.daily_json_to_dataframe(shzs)
        # 将乐视的数据合并至上证数据。由于其中从 2017-04-14 至 2018-01-23 之间停牌，所以 Close 数据为 NaN，需要补齐
        df = df_shzs.join(df_lee)
        print(df['300104'])
        df['300104'].plot()
        plt.show()
        # 先向前填充，后先后填充
        df = df.fillna(method='ffill').fillna(method='bfill')
        print(df['300104'])
        df['300104'].plot()
        plt.show()


if __name__ == '__main__':
    unittest.main()
