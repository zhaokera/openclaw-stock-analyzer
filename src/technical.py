#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
A股技术分析模块
"""

import json
import requests
import numpy as np
from datetime import datetime
from typing import Dict, Any, List, Optional
from .quote import QuoteAnalyzer

class TechnicalAnalyzer:
    def __init__(self):
        self.quote_analyzer = QuoteAnalyzer()
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        })
    
    def _get_historical_data(self, symbol: str, days: int = 60) -> List[Dict[str, Any]]:
        """获取历史K线数据"""
        try:
            # 转换symbol格式
            if symbol.startswith('sh'):
                em_symbol = f"1.{symbol[2:]}"
            elif symbol.startswith('sz'):
                em_symbol = f"0.{symbol[2:]}"
            else:
                em_symbol = symbol
            
            # 东方财富历史数据API
            url = f'https://push2his.eastmoney.com/api/qt/stock/kline/get?secid={em_symbol}&fields1=f1,f2,f3,f4,f5&fields2=f51,f52,f53,f54,f55,f56,f57,f58,f59,f60,f61&klt=101&fqt=1&end=20500101&lmt={days}'
            response = self.session.get(url, timeout=10)
            response.raise_for_status()
            
            data = response.json()
            if 'data' not in data or 'klines' not in data['data']:
                return []
            
            klines = data['data']['klines']
            historical_data = []
            
            for kline in klines:
                parts = kline.split(',')
                if len(parts) >= 6:
                    historical_data.append({
                        'date': parts[0],
                        'open': float(parts[1]),
                        'close': float(parts[2]),
                        'high': float(parts[3]),
                        'low': float(parts[4]),
                        'volume': int(float(parts[5]))
                    })
            
            return historical_data[-days:]  # 返回最近days天的数据
            
        except Exception as e:
            print(f"Error fetching historical data for {symbol}: {e}")
            return []
    
    def _calculate_ma(self, prices: List[float], period: int) -> float:
        """计算移动平均线"""
        if len(prices) < period:
            return 0.0
        return round(sum(prices[-period:]) / period, 2)
    
    def _calculate_macd(self, prices: List[float]) -> Dict[str, float]:
        """计算MACD指标"""
        if len(prices) < 26:
            return {"dif": 0.0, "dea": 0.0, "bar": 0.0}
        
        # 计算EMA12和EMA26
        ema12 = self._calculate_ema(prices, 12)
        ema26 = self._calculate_ema(prices, 26)
        
        dif = ema12[-1] - ema26[-1]
        dea = sum([ema12[i] - ema26[i] for i in range(max(0, len(ema12)-9), len(ema12))]) / min(9, len(ema12))
        bar = 2 * (dif - dea)
        
        return {
            "dif": round(dif, 2),
            "dea": round(dea, 2),
            "bar": round(bar, 2)
        }
    
    def _calculate_ema(self, prices: List[float], period: int) -> List[float]:
        """计算指数移动平均线"""
        if len(prices) < period:
            return [0.0] * len(prices)
        
        ema = [0.0] * len(prices)
        ema[period-1] = sum(prices[:period]) / period
        
        multiplier = 2 / (period + 1)
        for i in range(period, len(prices)):
            ema[i] = (prices[i] - ema[i-1]) * multiplier + ema[i-1]
        
        return ema
    
    def _calculate_rsi(self, prices: List[float]) -> Dict[str, float]:
        """计算RSI指标"""
        if len(prices) < 24:
            return {"rsi6": 0.0, "rsi12": 0.0, "rsi24": 0.0}
        
        def calculate_rsi_period(price_list, period):
            if len(price_list) < period + 1:
                return 0.0
            
            gains = []
            losses = []
            for i in range(1, len(price_list)):
                change = price_list[i] - price_list[i-1]
                if change > 0:
                    gains.append(change)
                    losses.append(0)
                else:
                    gains.append(0)
                    losses.append(abs(change))
            
            avg_gain = sum(gains[-period:]) / period
            avg_loss = sum(losses[-period:]) / period
            
            if avg_loss == 0:
                return 100.0 if avg_gain > 0 else 0.0
            
            rs = avg_gain / avg_loss
            rsi = 100 - (100 / (1 + rs))
            return round(rsi, 2)
        
        return {
            "rsi6": calculate_rsi_period(prices, 6),
            "rsi12": calculate_rsi_period(prices, 12),
            "rsi24": calculate_rsi_period(prices, 24)
        }
    
    def _calculate_kdj(self, highs: List[float], lows: List[float], closes: List[float]) -> Dict[str, float]:
        """计算KDJ指标"""
        if len(closes) < 9:
            return {"k": 0.0, "d": 0.0, "j": 0.0}
        
        # 计算RSV
        period = 9
        rsv_values = []
        for i in range(period-1, len(closes)):
            high_9 = max(highs[i-period+1:i+1])
            low_9 = min(lows[i-period+1:i+1])
            close = closes[i]
            if high_9 == low_9:
                rsv = 50.0
            else:
                rsv = (close - low_9) / (high_9 - low_9) * 100
            rsv_values.append(rsv)
        
        if not rsv_values:
            return {"k": 0.0, "d": 0.0, "j": 0.0}
        
        # 计算K、D、J
        k_values = [50.0]  # 初始值
        d_values = [50.0]  # 初始值
        
        for rsv in rsv_values:
            k = (2/3) * k_values[-1] + (1/3) * rsv
            d = (2/3) * d_values[-1] + (1/3) * k
            k_values.append(k)
            d_values.append(d)
        
        k = k_values[-1]
        d = d_values[-1]
        j = 3 * k - 2 * d
        
        return {
            "k": round(k, 2),
            "d": round(d, 2),
            "j": round(j, 2)
        }
    
    def _calculate_bollinger_bands(self, prices: List[float]) -> Dict[str, float]:
        """计算布林带"""
        if len(prices) < 20:
            current_price = prices[-1] if prices else 0.0
            return {
                "upper": current_price,
                "middle": current_price,
                "lower": current_price
            }
        
        period = 20
        ma20 = self._calculate_ma(prices, period)
        std_dev = np.std(prices[-period:])
        
        upper = ma20 + (std_dev * 2)
        lower = ma20 - (std_dev * 2)
        
        return {
            "upper": round(upper, 2),
            "middle": round(ma20, 2),
            "lower": round(lower, 2)
        }
    
    def _generate_signal(self, indicators: Dict[str, Any]) -> str:
        """生成交易信号"""
        signals = []
        
        # MACD信号
        macd = indicators.get('macd', {})
        if macd.get('dif', 0) > macd.get('dea', 0):
            signals.append('MACD金叉')
        
        # RSI信号
        rsi = indicators.get('rsi', {})
        if rsi.get('rsi6', 0) < 30:
            signals.append('RSI超卖')
        elif rsi.get('rsi6', 0) > 70:
            signals.append('RSI超买')
        
        # KDJ信号
        kdj = indicators.get('kdj', {})
        if kdj.get('k', 0) < 20 and kdj.get('d', 0) < 20:
            signals.append('KDJ超卖')
        elif kdj.get('k', 0) > 80 and kdj.get('d', 0) > 80:
            signals.append('KDJ超买')
        
        # 布林带信号
        boll = indicators.get('boll', {})
        current_price = indicators.get('current_price', 0)
        if current_price <= boll.get('lower', 0):
            signals.append('触及下轨')
        elif current_price >= boll.get('upper', 0):
            signals.append('触及上轨')
        
        if any('超卖' in s or '金叉' in s or '下轨' in s for s in signals):
            return '买入'
        elif any('超买' in s or '死叉' in s or '上轨' in s for s in signals):
            return '卖出'
        else:
            return '观望'
    
    def technical_analysis(self, symbol: str, indicators: List[str] = None) -> Dict[str, Any]:
        """执行技术分析"""
        if indicators is None:
            indicators = ['ma', 'macd', 'rsi', 'kdj', 'boll']
        
        # 获取当前行情
        quote_data = self.quote_analyzer.get_quote(symbol)
        current_price = quote_data.get('current_price', 0)
        stock_name = quote_data.get('stock_name', '')
        
        if current_price <= 0:
            return {
                "symbol": symbol,
                "stock_name": stock_name,
                "current_price": current_price,
                "ma5": 0.0,
                "ma10": 0.0,
                "ma20": 0.0,
                "ma60": 0.0,
                "macd": {"dif": 0.0, "dea": 0.0, "bar": 0.0},
                "rsi": {"rsi6": 0.0, "rsi12": 0.0, "rsi24": 0.0},
                "kdj": {"k": 0.0, "d": 0.0, "j": 0.0},
                "boll": {"upper": 0.0, "middle": 0.0, "lower": 0.0},
                "volume_ma5": 0,
                "volume_ma10": 0,
                "signal": "数据不足"
            }
        
        # 获取历史数据
        historical_data = self._get_historical_data(symbol, 60)
        if not historical_data:
            return {
                "symbol": symbol,
                "stock_name": stock_name,
                "current_price": current_price,
                "ma5": 0.0,
                "ma10": 0.0,
                "ma20": 0.0,
                "ma60": 0.0,
                "macd": {"dif": 0.0, "dea": 0.0, "bar": 0.0},
                "rsi": {"rsi6": 0.0, "rsi12": 0.0, "rsi24": 0.0},
                "kdj": {"k": 0.0, "d": 0.0, "j": 0.0},
                "boll": {"upper": 0.0, "middle": 0.0, "lower": 0.0},
                "volume_ma5": 0,
                "volume_ma10": 0,
                "signal": "历史数据不足"
            }
        
        # 提取价格和成交量数据
        prices = [item['close'] for item in historical_data]
        volumes = [item['volume'] for item in historical_data]
        highs = [item['high'] for item in historical_data]
        lows = [item['low'] for item in historical_data]
        
        result = {
            "symbol": symbol,
            "stock_name": stock_name,
            "current_price": current_price
        }
        
        # 计算各项技术指标
        if 'ma' in indicators:
            result['ma5'] = self._calculate_ma(prices, 5)
            result['ma10'] = self._calculate_ma(prices, 10)
            result['ma20'] = self._calculate_ma(prices, 20)
            result['ma60'] = self._calculate_ma(prices, 60)
            result['volume_ma5'] = int(self._calculate_ma(volumes, 5))
            result['volume_ma10'] = int(self._calculate_ma(volumes, 10))
        
        if 'macd' in indicators:
            result['macd'] = self._calculate_macd(prices)
        
        if 'rsi' in indicators:
            result['rsi'] = self._calculate_rsi(prices)
        
        if 'kdj' in indicators:
            result['kdj'] = self._calculate_kdj(highs, lows, prices)
        
        if 'boll' in indicators:
            result['boll'] = self._calculate_bollinger_bands(prices)
        
        # 生成交易信号
        result['signal'] = self._generate_signal(result)
        
        return result