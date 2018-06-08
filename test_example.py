# Copyright (C) 2018 GuQiangJs.
# Licensed under https://www.gnu.org/licenses/gpl-3.0.html <see LICENSE file>

from datas import capture
import pandas
import datetime
import unittest
import os

TEST_FOLDER=os.path.join('testdatas','dailies')

class Test_example(unittest.TestCase):
    def setUp(self):
        """
        当数据不存在时，自动在testdatas目录下的dailies目录中增加 000001,000002 的每日成交汇总csv文件

        处理顺序：

        1. 使用 `datas.capture.online_daily_sohu` 方法获取指定数据。

        2. 使用 `pandas.DataFrame` 构建数据表，并将数据表保存。
        :return:
        """
        if not os.path.exists(TEST_FOLDER):
            os.makedirs(TEST_FOLDER,exist_ok=True)

        symbols=['000001','000002']
        for symbol in symbols:
            filename=os.path.join(TEST_FOLDER,'{0}.csv'.format(symbol))
            if not os.path.isfile(filename):
                re = capture().online_daily_sohu(symbol, start_date=datetime.date(2010, 1, 1),
                                                 end_date=datetime.date(2017, 12, 31))
                # 使用二维数组构建 `pands.DataFrame` ，并按照顺序指定列头
                pd = pandas.DataFrame(re[0]['hq'],columns=['Date','Open','Close','Change','Quote','Low','High','Volume','Turnover','Rate'])
                # 保存 `pandas.DataFrame` 至 `csv` 格式。跳过索引列
                pd.to_csv(filename,mode='w+',encoding='utf-8',index=False)

    def test1(self):
        pass