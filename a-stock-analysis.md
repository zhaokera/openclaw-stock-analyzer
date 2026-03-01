# Skill: A股实时分析

## 描述
实时分析A股市场，提供行情数据、技术指标、基本面分析和资金流向分析。

## 权限
- bash

## 功能

### 1. 实时行情
获取股票的最新价格、涨跌幅、成交量、成交额、委比、换手率等数据。

### 2. 技术分析
提供 K线、MACD、RSI、KDJ、布林带、均线系统等技术指标分析。

### 3. 基本面分析
分析市盈率、市净率、每股收益、每股净资产、总市值、流通市值等基本面指标。

### 4. 资金流向
监测主力资金、北向资金、散户资金等资金流向数据。

### 5. 同行对比
提供同行业公司的市盈率对比、票房对比。

### 6. 龙虎榜
提供当日龙虎榜数据，显示买卖前五的营业部信息。

## API 数据源

### 新浪财经 API
- 实时行情：`https://finance.sina.com.cn/api/quote.php?symbol=sh600000`
- 历史行情：`https://finance.sina.com.cn/api/quotes.php?symbol=sh600000&start=20240101&end=20241231`
- 龙虎榜：`https://finance.sina.com.cn/api/limitup.php`

### 东方财富 API
- 实时行情：`https://push2.eastmoney.com/api/qt/stock/get?secid=1.600000`
- 资金流向：`https://push2his.eastmoney.com/api/qt/stock/fflow/daykline?secid=1.600000`
- 基本资料：`https://emdata.guard.icbc.com.cn/api/data?code=600000`

### 淘财它 API
- 股票列表：`https://api.wt-bibi.com/api/stock/list`
- 实时行情：`https://api.wt-bibi.com/api/stock/quote`

## 使用示例

```
# 获取实时行情
skill: a-stock-analysis
action: get_quote
symbol: sh600000

# 技术分析
skill: a-stock-analysis
action: technical_analysis
symbol: sz000001
indicator: macd,rsi,kdj

# 基本面分析
skill: a-stock-analysis
action: fundamental_analysis
symbol: sh600000

# 资金流向
skill: a-stock-analysis
action: fund_flow
symbol: sz000001
period: 5d,10d,20d

# 龙虎榜
skill: a-stock-analysis
action: dragon_tiger_list
date: 2024-01-15

# 同行对比
skill: a-stock-analysis
action: peer_comparison
symbol: sh600000
```

## 输出格式

### 实时行情输出
```json
{
  "symbol": "sh600000",
  "stock_name": "浦发银行",
  "current_price": 10.50,
  "prev_close": 10.45,
  "open": 10.48,
  "high": 10.55,
  "low": 10.45,
  "volume": 125000000,
  "amount": 1312500000,
  "change_percent": 0.48,
  "change_amount": 0.05,
  "turnover_rate": 0.85,
  "p/e_ratio": 5.23,
  "p/b_ratio": 0.58,
  "bid_price": 10.49,
  "ask_price": 10.50,
  "bid_volume": 10000,
  "ask_volume": 20000,
  "circulating_market_cap": 985.0,
  "total_market_cap": 985.0,
  "date": "2024-01-15",
  "time": "14:30:00"
}
```

### 技术分析输出
```json
{
  "symbol": "sz000001",
  "stock_name": "平安银行",
  "current_price": 12.50,
  "ma5": 12.45,
  "ma10": 12.38,
  "ma20": 12.25,
  "ma60": 12.10,
  "macd": {
    "dif": 0.05,
    "dea": 0.03,
    "bar": 0.04
  },
  "rsi": {
    "rsi6": 65.5,
    "rsi12": 62.3,
    "rsi24": 58.7
  },
  "kdj": {
    "k": 75.2,
    "d": 68.5,
    "j": 88.6
  },
  "boll": {
    "upper": 12.80,
    "middle": 12.50,
    "lower": 12.20
  },
  "volume_ma5": 50000000,
  "volume_ma10": 48000000,
  "signal": "买入"
}
```

### 基本面分析输出
```json
{
  "symbol": "sh600000",
  "stock_name": "浦发银行",
  "eps": 1.25,
  "bps": 8.50,
  "pe_ttm": 8.40,
  "pe_ratio": 5.23,
  "pb_ratio": 0.58,
  "roa": 0.85,
  "roe": 12.50,
  "gross_profit_rate": 35.20,
  "net_profit_rate": 28.50,
  "total_assets": 15000.0,
  "circulating_market_cap": 985.0,
  "total_market_cap": 985.0,
  "revenue": 2500.0,
  "net_profit": 750.0,
  "revenue_growth": 5.50,
  "profit_growth": 3.20,
  "dividend_yield": 5.80,
  "很有名": 0.45
}
```

### 资金流向输出
```json
{
  "symbol": "sz000001",
  "stock_name": "平安银行",
  "current_price": 12.50,
  "change_percent": 1.20,
  "time": "2024-01-15 15:00:00",
  "fund_flow": {
    "latest": {
      "main_net": 1250.5,
      "super_net": 850.2,
      "big_net": 600.8,
      "middle_net": 350.3,
      "small_net": -50.8
    },
    "5_days": {
      "main_net": 3500.2,
      "super_net": 2200.5,
      "big_net": 1500.3,
      "middle_net": 900.2,
      "small_net": -200.5
    },
    "10_days": {
      "main_net": 5000.8,
      "super_net": 3000.2,
      "big_net": 2000.5,
      "middle_net": 1200.3,
      "small_net": -300.2
    },
    "20_days": {
      "main_net": 8500.5,
      "super_net": 5500.8,
      "big_net": 3500.2,
      "middle_net": 2200.5,
      "small_net": -500.3
    }
  },
  "signal": "主力资金流入"
}
```

### 龙虎榜输出
```json
{
  "date": "2024-01-15",
  "list": [
    {
      "symbol": "sh600000",
      "stock_name": "浦发银行",
      "current_price": 10.50,
      "change_percent": 10.02,
      "reason": "日涨幅超过10%",
      "buy_brokerage": [
        {"rank": 1, "name": "华泰证券上海捧乐路", "amount": 5000.5, "ratio": 15.2},
        {"rank": 2, "name": "中信证券杭州延安路", "amount": 3500.2, "ratio": 10.6},
        {"rank": 3, "name": "东吴证券苏州trade", "amount": 2800.3, "ratio": 8.5},
        {"rank": 4, "name": "国泰君安上海营业部", "amount": 2500.8, "ratio": 7.6},
        {"rank": 5, "name": "银河证券北京建国路", "amount": 2200.5, "ratio": 6.7}
      ],
      "sell_brokerage": [
        {"rank": 1, "name": "Chase Manhattan Capital", "amount": 4500.2, "ratio": 13.6},
        {"rank": 2, "name": "高盛高华证券北京长安街", "amount": 3200.5, "ratio": 9.7},
        {"rank": 3, "name": "摩根士丹利华鑫上海trade", "amount": 2800.3, "ratio": 8.5},
        {"rank": 4, "name": "瑞银证券上海营业部", "amount": 2500.8, "ratio": 7.6},
        {"rank": 5, "name": "花旗银行上海分行", "amount": 2200.5, "ratio": 6.7}
      ],
      "net_amount": 1500.3,
      "total_amount": 21300.5
    }
  ],
  "total_count": 15
}
```

## 警告和注意事项

1. API 可能存在调用频率限制，请合理控制请求频率。
2. 免费 API 数据可能存在延迟，不适合高频交易。
3. 股票数据仅供参考，不构成投资建议。
4. 请注意数据格式的变化，及时更新解析逻辑。
5. 部分历史数据可能需要付费获取。

## 扩展功能

1. **股票筛选器**：根据条件筛选股票，如市盈率低于10、市净率低于1、市值小于100亿等。
2. **自定义监控列表**：支持用户维护自己的监控列表，并定期推送行情。
3. ** alerts**：当股票价格突破设定区间时发送通知。
4. **新闻推送**：抓取相关股票的新闻资讯。
5. **财务报表**：抓取季报、年报、中报等财务报表数据。
6. **股东研究**：分析股东人数、十大股东、十大流通股东等变化。
7. **机构评级**：获取机构的买入/持有/卖出评级。
8. **限售解禁**：提示即将解禁的限售股信息。
9. **分红送股**：记录分红送股等除权除息信息。
10. **涨跌停分析**：统计涨跌停股票数量和分布。

## 维护者
Claude Code

## 版本
v1.0.0

## 更新日志

### v1.0.0 (2024-01-15)
- 初始版本发布
- 实现实时行情、技术分析、基本面分析、资金流向、龙虎榜等功能
