#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
A股实时行情模块
"""

import json
import requests
import time
from datetime import datetime
from typing import Dict, Any, Optional

class QuoteAnalyzer:
    def __init__(self):
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        })
    
    def _normalize_symbol(self, symbol: str) -> str:
        """标准化股票代码格式"""
        symbol = symbol.lower().strip()
        if symbol.startswith(('sh', 'sz')):
            return symbol
        elif symbol.isdigit():
            if len(symbol) == 6:
                if symbol.startswith('6'):
                    return f'sh{symbol}'
                else:
                    return f'sz{symbol}'
        return symbol
    
    def _parse_sina_quote(self, symbol: str) -> Optional[Dict[str, Any]]:
        """解析新浪财经API数据"""
        try:
            # 新浪财经API URL
            url = f'https://hq.sinajs.cn/list={symbol}'
            response = self.session.get(url, timeout=10)
            response.raise_for_status()
            
            # 解析返回的数据
            data_str = response.text.strip()
            if not data_str or 'FAILED' in data_str or 'var hq_str_' not in data_str:
                return None
            
            # 提取数据部分
            start_idx = data_str.find('"') + 1
            end_idx = data_str.rfind('"')
            if start_idx <= 0 or end_idx <= 0:
                return None
            
            data_content = data_str[start_idx:end_idx]
            if not data_content:
                return None
                
            data_parts = data_content.split(',')
            if len(data_parts) < 33:
                # 尝试处理较短的数据格式
                if len(data_parts) >= 9:
                    # 基本字段：股票名称,今日开盘价,昨日收盘价,当前价格,最高价,最低价,成交股数,成交金额
                    stock_name = data_parts[0]
                    open_price = float(data_parts[1]) if data_parts[1] and data_parts[1] != '0' else 0.0
                    prev_close = float(data_parts[2]) if data_parts[2] and data_parts[2] != '0' else 0.0
                    current_price = float(data_parts[3]) if data_parts[3] and data_parts[3] != '0' else 0.0
                    high_price = float(data_parts[4]) if data_parts[4] and data_parts[4] != '0' else 0.0
                    low_price = float(data_parts[5]) if data_parts[5] and data_parts[5] != '0' else 0.0
                    volume = int(data_parts[6]) if data_parts[6] and data_parts[6] != '0' else 0
                    amount = float(data_parts[7]) if data_parts[7] and data_parts[7] != '0' else 0.0
                    
                    # 计算涨跌幅和涨跌额
                    change_amount = current_price - prev_close if prev_close > 0 else 0.0
                    change_percent = (change_amount / prev_close * 100) if prev_close > 0 else 0.0
                    
                    # 设置默认值
                    bid_price = current_price
                    ask_price = current_price
                    bid_volume = 0
                    ask_volume = 0
                    turnover_rate = 0.0
                    pe_ratio = 0.0
                    pb_ratio = 0.0
                    circulating_market_cap = 0.0
                    total_market_cap = 0.0
                    
                    # 日期和时间
                    current_time = datetime.now()
                    date_str = current_time.strftime('%Y-%m-%d')
                    time_str = current_time.strftime('%H:%M:%S')
                    
                    return {
                        "symbol": symbol,
                        "stock_name": stock_name,
                        "current_price": round(current_price, 2),
                        "prev_close": round(prev_close, 2),
                        "open": round(open_price, 2),
                        "high": round(high_price, 2),
                        "low": round(low_price, 2),
                        "volume": volume,
                        "amount": round(amount, 2),
                        "change_percent": round(change_percent, 2),
                        "change_amount": round(change_amount, 2),
                        "turnover_rate": round(turnover_rate, 2),
                        "p/e_ratio": round(pe_ratio, 2),
                        "p/b_ratio": round(pb_ratio, 2),
                        "bid_price": round(bid_price, 2),
                        "ask_price": round(ask_price, 2),
                        "bid_volume": bid_volume,
                        "ask_volume": ask_volume,
                        "circulating_market_cap": round(circulating_market_cap, 2),
                        "total_market_cap": round(total_market_cap, 2),
                        "date": date_str,
                        "time": time_str
                    }
                return None
            
            # 解析完整的数据格式
            stock_name = data_parts[0]
            current_price = float(data_parts[3]) if data_parts[3] and data_parts[3] != '0' else 0.0
            prev_close = float(data_parts[2]) if data_parts[2] and data_parts[2] != '0' else 0.0
            open_price = float(data_parts[1]) if data_parts[1] and data_parts[1] != '0' else 0.0
            high_price = float(data_parts[4]) if data_parts[4] and data_parts[4] != '0' else 0.0
            low_price = float(data_parts[5]) if data_parts[5] and data_parts[5] != '0' else 0.0
            volume = int(data_parts[8]) if data_parts[8] and data_parts[8] != '0' else 0
            amount = float(data_parts[9]) if data_parts[9] and data_parts[9] != '0' else 0.0
            
            # 计算涨跌幅和涨跌额
            change_amount = current_price - prev_close if prev_close > 0 else 0.0
            change_percent = (change_amount / prev_close * 100) if prev_close > 0 else 0.0
            
            # 委买委卖价格和数量（简化处理）
            bid_price = float(data_parts[10]) if data_parts[10] and data_parts[10] != '0' else current_price
            ask_price = float(data_parts[22]) if data_parts[22] and data_parts[22] != '0' else current_price
            bid_volume = int(data_parts[11]) if data_parts[11] and data_parts[11] != '0' else 0
            ask_volume = int(data_parts[23]) if data_parts[23] and data_parts[23] != '0' else 0
            
            # 换手率（需要额外计算，这里用成交量/流通股本估算，暂时设为0）
            turnover_rate = 0.0
            
            # 市盈率、市净率（新浪数据中可能不包含，需要其他来源）
            pe_ratio = 0.0
            pb_ratio = 0.0
            
            # 市值（需要额外数据，暂时设为0）
            circulating_market_cap = 0.0
            total_market_cap = 0.0
            
            # 日期和时间
            date_str = data_parts[30] if len(data_parts) > 30 and data_parts[30] else datetime.now().strftime('%Y-%m-%d')
            time_str = data_parts[31] if len(data_parts) > 31 and data_parts[31] else datetime.now().strftime('%H:%M:%S')
            
            return {
                "symbol": symbol,
                "stock_name": stock_name,
                "current_price": round(current_price, 2),
                "prev_close": round(prev_close, 2),
                "open": round(open_price, 2),
                "high": round(high_price, 2),
                "low": round(low_price, 2),
                "volume": volume,
                "amount": round(amount, 2),
                "change_percent": round(change_percent, 2),
                "change_amount": round(change_amount, 2),
                "turnover_rate": round(turnover_rate, 2),
                "p/e_ratio": round(pe_ratio, 2),
                "p/b_ratio": round(pb_ratio, 2),
                "bid_price": round(bid_price, 2),
                "ask_price": round(ask_price, 2),
                "bid_volume": bid_volume,
                "ask_volume": ask_volume,
                "circulating_market_cap": round(circulating_market_cap, 2),
                "total_market_cap": round(total_market_cap, 2),
                "date": date_str,
                "time": time_str
            }
            
        except Exception as e:
            print(f"Error parsing Sina quote for {symbol}: {e}")
            return None
    
    def _parse_eastmoney_quote(self, symbol: str) -> Optional[Dict[str, Any]]:
        """解析东方财富API数据"""
        try:
            # 转换symbol格式（东方财富使用1.或0.前缀）
            em_symbol = symbol
            if symbol.startswith('sh'):
                em_symbol = f"1.{symbol[2:]}"
            elif symbol.startswith('sz'):
                em_symbol = f"0.{symbol[2:]}"
            
            # 东方财富API URL
            url = f'https://push2.eastmoney.com/api/qt/stock/get?secid={em_symbol}&fields=f58,f107,f57,f43,f169,f170,f152,f177,f111,f46,f60,f44,f45,f47,f260,f261,f279,f280,f19,f17,f15,f13,f11,f20,f18,f16,f14,f12,f39,f250,f251'
            response = self.session.get(url, timeout=10)
            response.raise_for_status()
            
            data = response.json()
            if 'data' not in data or data['data'] is None:
                return None
            
            stock_data = data['data']
            
            # 提取基本字段
            stock_name = stock_data.get('f58', '')
            current_price = float(stock_data.get('f43', 0))
            prev_close = float(stock_data.get('f169', 0))
            open_price = float(stock_data.get('f170', 0))
            high_price = float(stock_data.get('f152', 0))
            low_price = float(stock_data.get('f177', 0))
            volume = int(stock_data.get('f111', 0))
            amount = float(stock_data.get('f46', 0))
            
            # 计算涨跌幅
            change_amount = current_price - prev_close if prev_close > 0 else 0.0
            change_percent = (change_amount / prev_close * 100) if prev_close > 0 else 0.0
            
            # 委买委卖
            bid_price = float(stock_data.get('f260', current_price))
            ask_price = float(stock_data.get('f261', current_price))
            bid_volume = int(stock_data.get('f279', 0))
            ask_volume = int(stock_data.get('f280', 0))
            
            # 换手率
            turnover_rate = float(stock_data.get('f19', 0))
            
            # 市盈率、市净率
            pe_ratio = float(stock_data.get('f17', 0))
            pb_ratio = float(stock_data.get('f15', 0))
            
            # 市值
            circulating_market_cap = float(stock_data.get('f13', 0)) / 1e8  # 转换为亿
            total_market_cap = float(stock_data.get('f11', 0)) / 1e8  # 转换为亿
            
            # 日期和时间
            current_time = datetime.now()
            date_str = current_time.strftime('%Y-%m-%d')
            time_str = current_time.strftime('%H:%M:%S')
            
            return {
                "symbol": symbol,
                "stock_name": stock_name,
                "current_price": round(current_price, 2),
                "prev_close": round(prev_close, 2),
                "open": round(open_price, 2),
                "high": round(high_price, 2),
                "low": round(low_price, 2),
                "volume": volume,
                "amount": round(amount, 2),
                "change_percent": round(change_percent, 2),
                "change_amount": round(change_amount, 2),
                "turnover_rate": round(turnover_rate, 2),
                "p/e_ratio": round(pe_ratio, 2),
                "p/b_ratio": round(pb_ratio, 2),
                "bid_price": round(bid_price, 2),
                "ask_price": round(ask_price, 2),
                "bid_volume": bid_volume,
                "ask_volume": ask_volume,
                "circulating_market_cap": round(circulating_market_cap, 2),
                "total_market_cap": round(total_market_cap, 2),
                "date": date_str,
                "time": time_str
            }
            
        except Exception as e:
            print(f"Error parsing EastMoney quote for {symbol}: {e}")
            return None
    
    def get_quote(self, symbol: str) -> Dict[str, Any]:
        """获取实时行情数据"""
        normalized_symbol = self._normalize_symbol(symbol)
        
        # 首先尝试东方财富API（数据更完整）
        quote_data = self._parse_eastmoney_quote(normalized_symbol)
        if quote_data and quote_data.get('current_price', 0) > 0:
            return quote_data
        
        # 如果东方财富失败，尝试新浪财经API
        quote_data = self._parse_sina_quote(normalized_symbol)
        if quote_data and quote_data.get('current_price', 0) > 0:
            return quote_data
        
        # 如果都失败，返回空数据结构
        return {
            "symbol": normalized_symbol,
            "stock_name": "",
            "current_price": 0.0,
            "prev_close": 0.0,
            "open": 0.0,
            "high": 0.0,
            "low": 0.0,
            "volume": 0,
            "amount": 0.0,
            "change_percent": 0.0,
            "change_amount": 0.0,
            "turnover_rate": 0.0,
            "p/e_ratio": 0.0,
            "p/b_ratio": 0.0,
            "bid_price": 0.0,
            "ask_price": 0.0,
            "bid_volume": 0,
            "ask_volume": 0,
            "circulating_market_cap": 0.0,
            "total_market_cap": 0.0,
            "date": datetime.now().strftime('%Y-%m-%d'),
            "time": datetime.now().strftime('%H:%M:%S')
        }