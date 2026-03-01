# openclaw-stock-analyzer

A股实时分析 Skill，为 Claude Code 提供专业的 A 股市场分析能力。

## 功能特性

### 📊 实时行情
获取股票的最新价格、涨跌幅、成交量、成交额、委比、换手率等数据。

| 指标 | 说明 |
|------|------|
| `current_price` | 最新价格 |
| `prev_close` | 昨日收盘价 |
| `open` | 今日开盘价 |
| `high` | 最高价 |
| `low` | 最低价 |
| `volume` | 成交量 |
| `amount` | 成交额 |
| `change_percent` | 涨跌幅 |
| `change_amount` | 涨跌额 |
| `turnover_rate` | 换手率 |
| `p/e_ratio` | 市盈率 |
| `p/b_ratio` | 市净率 |
| `bid_price` | 买一价 |
| `ask_price` | 卖一价 |
| `bid_volume` | 买一量 |
| `ask_volume` | 卖一量 |

### 📈 技术分析
提供 K线、MACD、RSI、KDJ、布林带、均线系统等技术指标分析。

| 指标 | 说明 |
|------|------|
| `ma5` | 5日均线 |
| `ma10` | 10日均线 |
| `ma20` | 20日均线 |
| `ma60` | 60日均线 |
| `macd.dif` | DIF线 |
| `macd.dea` | DEA线 |
| `macd.bar` | MACD柱 |
| `rsi6/12/24` | 6/12/24日RSI |
| `kdj.k/d/j` | KDJ指标 |
| `boll.upper/middle/lower` | 布林带上下轨 |

### 📉 基本面分析
分析市盈率、市净率、每股收益、每股净资产、总市值、流通市值等基本面指标。

| 指标 | 说明 |
|------|------|
| `eps` | 每股收益 |
| `bps` | 每股净资产 |
| `pe_ratio` | 市盈率 |
| `pb_ratio` | 市净率 |
| `roe` | 净资产收益率 |
| `roa` | 总资产收益率 |
| `gross_profit_rate` | 毛利率 |
| `net_profit_rate` | 净利润率 |
| `revenue_growth` | 营收增长率 |
| `profit_growth` | 利润增长率 |
| `dividend_yield` | 股息率 |

### 💰 资金流向
监测主力资金、北向资金、散户资金等资金流向数据。

| 资金类型 | 说明 |
|----------|------|
| `main_net` | 主力资金净额 |
| `super_net` | 超大单资金净额 |
| `big_net` | 大单资金净额 |
| `middle_net` | 中单资金净额 |
| `small_net` | 小单资金净额 |

### 🏆 龙虎榜
提供当日龙虎榜数据，显示买卖前五的营业部信息。

| 字段 | 说明 |
|------|------|
| `buy_brokerage` | 买五营业部 |
| `sell_brokerage` | 卖五营业部 |
| `net_amount` | 净额 |
| `total_amount` | 总额 |
| `reason` | 龙虎榜原因 |

### 🔍 股票搜索
支持通过关键词搜索股票，支持股票代码、股票名称搜索。

### 📊 同行对比
提供同行业公司的市盈率、市净率、市值等对比分析。

## 安装使用

### 安装到 Claude Code

1. 将 `a-stock-analysis.md` 文件复制到 Claude Code 的 skills 目录
   - macOS: `~/Library/Application Support/Claude/skills/`
   - Windows: `%APPDATA%\Claude\skills\`
   - Linux: `~/.config/Claude/skills/`

2. 重启 Claude Code 或重新加载 skills

### 使用示例

```
# 获取实时行情
skill: a-stock-analysis
action: get_quote
symbol: sh600000

# 获取技术分析
skill: a-stock-analysis
action: technical_analysis
symbol: sz000001
indicator: macd,rsi,kdj

# 获取基本面分析
skill: a-stock-analysis
action: fundamental_analysis
symbol: sh600000

# 获取资金流向
skill: a-stock-analysis
action: fund_flow
symbol: sz000001
period: 5d,10d,20d

# 获取龙虎榜
skill: a-stock-analysis
action: dragon_tiger_list
date: 2024-01-15

# 同行对比
skill: a-stock-analysis
action: peer_comparison
symbol: sh600000

# 股票搜索
skill: a-stock-analysis
action: search_stock
keyword: 贵州茅台
```

## 股票代码格式

- **上交所股票**: `sh` + 6位数字
  - `sh600000` - 浦发银行
  - `sh600519` - 贵州茅台
  - `sh601318` - 中国平安

- **深交所股票**: `sz` + 6位数字
  - `sz000001` - 平安银行
  - `sz000858` - 五粮液
  - `sz300750` - 宁德时代

## 输出格式

### 实时行情输出示例
```json
{
  "symbol": "sh600000",
  "stock_name": "浦发银行",
  "current_price": 10.50,
  "prev_close": 10.45,
  "change_percent": 0.48,
  "change_amount": 0.05,
  "volume": 125000000,
  "amount": 1312500000,
  "turnover_rate": 0.85,
  "p/e_ratio": 5.23,
  "p/b_ratio": 0.58,
  "date": "2024-01-15",
  "time": "14:30:00"
}
```

### 技术分析输出示例
```json
{
  "symbol": "sz000001",
  "stock_name": "平安银行",
  "current_price": 12.50,
  "ma5": 12.45,
  "ma10": 12.38,
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
  "signal": "买入"
}
```

### 龙虎榜输出示例
```json
{
  "date": "2024-01-15",
  "list": [
    {
      "symbol": "sh600000",
      "stock_name": "浦发银行",
      "change_percent": 10.02,
      "reason": "日涨幅超过10%",
      "buy_brokerage": [...],
      "sell_brokerage": [...]
    }
  ]
}
```

## 技术栈

- **语言**: Bash
- **数据源**: 新浪财经、东方财富
- **API**: 免费公开 API

## 数据源说明

### 新浪财经 API
- 实时行情：`https://finance.sina.com.cn/api/quote.php`
- 历史行情：`https://finance.sina.com.cn/api/quotes.php`
- 龙虎榜：`https://finance.sina.com.cn/api/limitup.php`

### 东方财富 API
- 实时行情：`https://push2.eastmoney.com/api/qt/stock/get`
- 资金流向：`https://push2his.eastmoney.com/api/qt/stock/fflow/daykline`
- 基本资料：`https://emdata.guard.icbc.com.cn/api/data`

## 注意事项

1. **数据延迟**: 免费 API 数据可能存在 1-5 分钟延迟，不适合高频交易
2. **调用频率**: 请合理控制请求频率，避免被限制
3. **数据准确性**: 数据仅供参考，不构成投资建议
4. **风险提示**: 股市有风险，投资需谨慎

## 相关项目

- [openclaw-finance-news](https://github.com/zhaokera/openclaw-finance-news) - 财经新闻 Skill

## 更新日志

### v1.0.0 (2024-01-15)
- 初始版本发布
- 实现实时行情、技术分析、基本面分析、资金流向、龙虎榜等功能

## 许可证

MIT License

## 作者

zhaokera

## 相关链接

- [新浪财经](https://finance.sina.com.cn/)
- [东方财富](https://www.eastmoney.com/)
- [Claude Code](https://claude.ai/)
