# Copyright (C) 2018 GuQiangJs.
# Licensed under https://www.gnu.org/licenses/gpl-3.0.html <see LICENSE file>

import datetime
import json

import pandas as pd
import requests


class translate():
    def daily_json_to_dataframe(json_str, index=['Date'],
                                columns=['Date', 'Open', 'Close', 'Change', 'Quote', 'Low', 'High', 'Volume',
                                         'Turnover', 'Rate'], sort_index: bool = True, ascending: bool = True):
        """
        每日成交汇总数据的 json 内容转 `pandas.DataFrame`

        取 json 内容中的 第一个元素中的 'hq' 的列表内容为表格

        * 程序会自动根据 `index` 参数设置返回的 `pandas.DataFrame` 的 索引

        * 程序会自动将 `Close` 列转换为 `float64` 类型。
            >> 如果以上列存在于 pandas.DataFrame` 中
        :param index: 索引列。默认为 `Date`
        :param columns: 读取列
        :param sort_index: 是否按照索引列排序。
        :param ascending: 排序规则。默认为 `True`。
        :return:
        """
        df = pd.DataFrame(json_str[0]['hq'], columns=columns)
        if index:
            df = df.set_index(index)
        if 'Close' in columns:
            df['Close'] = pd.to_numeric(df['Close'], downcast='signed')
        if sort_index:
            df = df.sort_index(ascending=ascending)
        return df


class capture():
    def online_daily_sohu_shzs(self, start_date: datetime.date = datetime.date(2004, 10, 8),
                               end_date: datetime.date = datetime.date.today() + datetime.timedelta(days=-1)):
        """
        从 搜狐 获取 **上证指数** 指定日期之间的每日成交汇总数据

        :param start_date: 开始日期。 默认值：2004-10-08

        :param end_date: 结束日期。如果不传入数据，会取当前日期的 **前一天** 作为默认值。

        :return: 返回按照 **交易日期反向排序** 的Json对象。

        参考 datas.capture.__online_daily_sohu__ 返回值示例
        """
        return self.__online_daily_sohu__('zs_000001', prefix='', start_date=start_date, end_date=end_date)

    def online_daily_sohu_szcz(self, start_date: datetime.date = datetime.date(2004, 10, 8),
                               end_date: datetime.date = datetime.date.today() + datetime.timedelta(days=-1)):
        """
        从 搜狐 获取 **深证成指** 指定日期之间的每日成交汇总数据

        :param start_date: 开始日期。 默认值：2004-10-08

        :param end_date: 结束日期。如果不传入数据，会取当前日期的 **前一天** 作为默认值。

        :return: 返回按照 **交易日期反向排序** 的Json对象。

        参考 datas.capture.__online_daily_sohu__ 返回值示例
        """
        return self.__online_daily_sohu__('zs_399001', prefix='', start_date=start_date, end_date=end_date)

    def online_daily_sohu(self, sybmol: str, prefix="cn_", start_date: datetime.date = datetime.date(2004, 10, 8),
                          end_date: datetime.date = datetime.date.today() + datetime.timedelta(days=-1)):
        """
        从 搜狐 获取 **指定股票** 指定日期之间的每日成交汇总数据

        :param sybmol: 指定的股票代码。For example: sz_000001(上证指数）,000002（万科）

        :param start_date: 开始日期。 默认值：2004-10-08

        :param end_date: 结束日期。如果不传入数据，会取当前日期的 **前一天** 作为默认值。

        :param prefix: 股票代码前缀。默认为 cn_。

        :return: 返回按照 **交易日期反向排序** 的Json对象。

        参考 datas.capture.__online_daily_sohu__ 返回值示例
        """
        return self.__online_daily_sohu__(sybmol, prefix=prefix, start_date=start_date, end_date=end_date)

    def __online_daily_sohu__(self, sybmol: str, prefix="cn_", start_date: datetime.date = datetime.date(2004, 10, 8),
                              end_date: datetime.date = datetime.date.today() + datetime.timedelta(days=-1)):
        """
        从 搜狐 获取指定日期之间的每日成交汇总数据

        :param sybmol: 指定的股票代码。For example: sz_000001(上证指数）,000002（万科）

        :param prefix: 股票代码前缀。默认为 cn_。

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

        Args:
            sybmol:
            prefix:
            start_date:
            end_date:
        """
        # http://q.stock.sohu.com/hisHq?code=cn_600569&start=20041008&end=20180608&stat=1&order=D&period=d&rt=jsonp
        context = self.__request_context__(
            'http://q.stock.sohu.com/hisHq?code={sybmol}&start={sds}&end={eds}&stat=1&order=D&period=d&rt=jsonp'.format(
                sybmol=prefix + sybmol, sds=start_date.strftime('%Y%m%d'), eds=end_date.strftime('%Y%m%d')))
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
