#!/usr/bin/python3
# -*- coding:utf-8 -*-
import akshare as ak
import tushare as ts

def test_ak():
    print(ak.__version__)
    stock_zh_a_hist_df = ak.stock_zh_a_hist(symbol="000001", period="daily", start_date="20220412", end_date="20230412",
                                            adjust="")
    print(stock_zh_a_hist_df)

import mplfinance as mpf
def plot_ak():
    stock_us_daily_df = ak.stock_us_daily(symbol="AAPL", adjust="qfq")
    stock_us_daily_df = stock_us_daily_df[["open", "high", "low", "close", "volume"]]
    stock_us_daily_df.columns = ["Open", "High", "Low", "Close", "Volume"]
    stock_us_daily_df.index.name = "Date"
    print(stock_us_daily_df)
    # stock_us_daily_df = stock_us_daily_df["2020-04-01": "2020-04-29"]
    mpf.plot(stock_us_daily_df, type='candle', mav=(3, 6, 9), volume=True, show_nontrading=False)
def test_ts():
    print(ts.__version__)
    ts.get_hist_data('600848')  # 一次性获取全部数据

if __name__ == '__main__':
    # test_ts()
    # test_ak()
    plot_ak()