# Copyright (C) 2018 GuQiangJs.
# Licensed under https://www.gnu.org/licenses/gpl-3.0.html <see LICENSE file>

import datetime
import unittest

import pandas

from datas import capture


class Test_capture(unittest.TestCase):
    def test_online_daily_sohu(self):
        """
        测试 `datas.capture.online_daily_sohu` 方法
        :return:
        """
        re = capture().online_daily_sohu('000002', start_date=datetime.date(2018, 6, 5),
                                         end_date=datetime.date(2018, 6, 8))
        self.assertTrue(re)
        print(re)
        self.assertEqual(1, len(re))
        self.assertTrue(re[0])
        self.assertTrue('status' in re[0])
        self.assertEqual(0, re[0]['status'])
        self.assertTrue('code' in re[0])
        self.assertEqual('cn_000002', re[0]['code'])
        self.assertTrue('hq' in re[0])
        self.assertEqual(4, len(re[0]['hq']))
        self.assertTrue('2018-06-08' in re[0]['hq'][0][0])
        self.assertTrue('2018-06-05' in re[0]['hq'][-1][0])

    def test_get_shzs(self):
        """
        测试获取上证指数
        :return:
        """
        re=capture().online_daily_sohu_shzs(start_date=datetime.date(2018, 6, 5),
                                         end_date=datetime.date(2018, 6, 8))
        self.assertTrue(re)
        print(re)


if __name__ == '__main__':
    unittest.main()
