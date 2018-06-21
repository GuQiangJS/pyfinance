# Copyright (C) 2018 GuQiangJs.
# Licensed under https://www.gnu.org/licenses/gpl-3.0.html <see LICENSE file>

import unittest

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

import test_helper


class MyTestCase(test_helper.MyTestBase):
    def test_01_06_05_plot_histogram(self):
        start_date = '2017-01-01'
        end_date = '2017-12-31'
        dates = pd.date_range(start_date, end_date)
        # 创建一个空的DataFrame
        df1 = pd.DataFrame(index=dates)
        # 读取 csv 文件到临时 DataFrame，只读取其中的 Date 列和 Close 列，索引列为 Date，转换空值为 nan，转换日期字段
        dfs = test_helper.read_symbol_daily('000002', ['Date', 'Close'], 'Date')
        df1 = df1.join(dfs, how='inner')
        self.__plot_data__(df1)

        # 计算日收益率
        daily_returns = test_helper.compute_daily_returns(df1)
        # 绘制收益率
        self.__plot_data__(daily_returns, title='Daily returns', ylable='Daily returns')

        # 绘制直方图
        daily_returns.hist()
        # 绘图
        # self.__plot_data__(daily_returns)

        # 计算均值
        mean = daily_returns['Close'].mean()
        print("mean={}".format(mean))
        # 计算标准差
        std = daily_returns['Close'].std()
        print("std={}".format(std))

        # 绘制均值线
        plt.axvline(mean, color='w', linestyle='dashed', linewidth=2)
        # 绘制标准差
        plt.axvline(std, color='r', linestyle='dashed', linewidth=2)
        plt.axvline(-std, color='r', linestyle='dashed', linewidth=2)

        # 绘图
        plt.show()

        # 计算峰度
        print("kurtosis={}".format(daily_returns['Close'].kurtosis()))

    def test_01_06_08_plot_two_histograms_together(self):
        start_date = '2017-01-01'
        end_date = '2017-12-31'
        dates = pd.date_range(start_date, end_date)
        # 创建一个空的DataFrame
        df1 = pd.DataFrame(index=dates)
        # 读取 csv 文件到临时 DataFrame，只读取其中的 Date 列和 Close 列，索引列为 Date，转换空值为 nan，转换日期字段
        dfs = test_helper.read_symbol_daily('000002', ['Date', 'Close'], 'Date')
        dfs = dfs.rename(columns={'Close': '000002'})
        df1 = df1.join(dfs, how='inner')
        dfs = test_helper.read_symbol_daily('000001', ['Date', 'Close'], 'Date')
        dfs = dfs.rename(columns={'Close': '000001'})
        df1 = df1.join(dfs, how='inner')

        # 计算日收益率
        daily_returns = test_helper.compute_daily_returns(df1)
        # 绘制直方图
        daily_returns.hist(bins=20)
        # 绘图
        plt.show()

        # 合并绘制两个直方图
        daily_returns['000001'].hist(bins=20, label='000001')
        daily_returns['000002'].hist(bins=20, label='000002')
        plt.legend(loc='upper right')
        plt.show()

    def test_01_06_13_scatterplots(self):
        # 一次读入三个数据。上证指数，000001,000002
        pdd = test_helper.read_symbol_daily_close(['zs_000001', '000001', '000002'], start_date='2017-01-01',
                                                  end_date='2017-12-31')
        # 绘制每日收盘价的归一化后图示
        test_helper.plot_data(test_helper.normalize_data(pdd))

        # 计算三个数据的日回报率
        daily_returns = test_helper.compute_daily_returns(pdd)
        test_helper.plot_data(daily_returns, title='日回报率', ylabel='日回报率')

        # 绘制散点图 (上证指数相对于000002)
        daily_returns.plot(kind='scatter', x='zs_000001', y='000002')
        # 计算α系数和β系数。绘制斜率
        # X轴为上证指数的日收益，Y轴为000002的日收益
        beta_2, alpha_2 = np.polyfit(daily_returns['zs_000001'], daily_returns['000002'], 1)
        # 当直线L的斜率存在时，对于一次函数y=kx+b（斜截式），k即该函数图像(直线)的斜率。
        plt.plot(daily_returns['zs_000001'], beta_2 * daily_returns['zs_000001'] + alpha_2, '-', color='r')
        plt.show()
        print('000002-beta:', beta_2)
        print('000002-alpha:', alpha_2)

        # 绘制散点图 (上证指数相对于000001)
        daily_returns.plot(kind='scatter', x='zs_000001', y='000001')
        beta_1, alpha_1 = np.polyfit(daily_returns['zs_000001'], daily_returns['000001'], 1)
        # 当直线L的斜率存在时，对于一次函数y=kx+b（斜截式），k即该函数图像(直线)的斜率。
        plt.plot(daily_returns['zs_000001'], beta_1 * daily_returns['zs_000001'] + alpha_1, '-', color='r')
        plt.show()
        print('000001-beta:', beta_1)
        print('000001-alpha:', alpha_1)

        # 相关性（拟合度）
        #             shzs    000001    000002
        #     shzs    1.000000  0.486895  0.206434
        #     000001  0.486895  1.000000  0.193329
        #     000002  0.206434  0.193329  1.000000
        print(daily_returns.corr(method='pearson'))


if __name__ == '__main__':
    unittest.main()
