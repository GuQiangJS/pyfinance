# Copyright (C) 2018 GuQiangJs.
# Licensed under https://www.gnu.org/licenses/gpl-3.0.html <see LICENSE file>

import datetime
import json

import requests


class capture():
    def online_daily_sohu(self, sybmol: str, start_date: datetime.date = datetime.date(2004, 10, 8),
                          end_date: datetime.date = datetime.date.today() + datetime.timedelta(days=-1)):
        """
        从 搜狐 获取指定日期之间的每日成交汇总数据

        :param sybmol: 指定的股票代码。For example:600001,000002,300002

        :param start_date: 开始日期。 默认值：2004-10-08

        :param end_date: 结束日期。如果不传入数据，会取当前日期的 **前一天** 作为默认值。

        :return: 返回按照 **交易日期反向排序** 的Json对象。
        For example:
        ::
            [
                {
                    "status": 0,
                    "hq": [
                        [
                            "2018-06-08",
                            "27.10",
                            "26.71",
                            "-0.68",
                            "-2.48%",
                            "26.55",
                            "27.18",
                            "388545",
                            "104050.16",
                            "0.40%"
                        ],
                        [
                            "2018-06-07",
                            "27.07",
                            "27.39",
                            "0.40",
                            "1.48%",
                            "26.95",
                            "27.64",
                            "597536",
                            "163791.83",
                            "0.62%"
                        ],
                        [
                            "2018-06-06",
                            "27.30",
                            "26.99",
                            "-0.50",
                            "-1.82%",
                            "26.85",
                            "27.54",
                            "508163",
                            "137842.73",
                            "0.52%"
                        ],
                        [
                            "2018-06-05",
                            "27.29",
                            "27.49",
                            "0.19",
                            "0.70%",
                            "26.84",
                            "27.77",
                            "606841",
                            "165847.34",
                            "0.62%"
                        ]
                    ],
                    "code": "cn_000002",
                    "stat": [
                        "ÀÛ¼Æ:",
                        "2018-06-05ÖÁ2018-06-08",
                        "-0.59",
                        "-2.16%",
                        26.55,
                        27.77,
                        2101085,
                        571532.06,
                        "2.16%"
                    ]
                }
            ]
        """
        # http://q.stock.sohu.com/hisHq?code=cn_600569&start=20041008&end=20180608&stat=1&order=D&period=d&rt=jsonp
        context = self.__request_context__(
            'http://q.stock.sohu.com/hisHq?code=cn_{sybmol}&start={sds}&end={eds}&stat=1&order=D&period=d&rt=jsonp'.format(
                sybmol=sybmol, sds=start_date.strftime('%Y%m%d'), eds=end_date.strftime('%Y%m%d')))
        txt = str(context, encoding='ISO-8859-9')
        return json.loads(txt[9:-2])

    def __request_context__(self, url, headers: {} = None, timeout: int = 30):
        rep = self.__request__(url, headers=headers, timeout=timeout)
        return rep.content

    def __request_text__(self, url, headers: {} = None, timeout: int = 30):
        rep = self.__request__(url, headers=headers, timeout=timeout)
        return rep.text

    def __request__(self, url, headers: {} = None, timeout: int = 30):
        return requests.get(url, timeout=timeout, headers=self.__fill_headers__(headers))

    def __fill_headers__(self, headers: {} = None):
        """
        填充 request 请求时使用的 headers
        :param headers:
        :return:
        """
        result = headers
        if not result:
            result = {}
        if 'User-Agent' not in result:
            result[
                'User-Agent'] = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/66.0.3359.181 Safari/537.36'
        if 'Accept-Encoding' not in result:
            result['Accept-Encoding'] = 'gzip, deflate'
        if 'Accept-Language' not in result:
            result['Accept-Language'] = 'zh-CN,zh;q=0.9,en;q=0.8,en-US;q=0.7'
        return result
