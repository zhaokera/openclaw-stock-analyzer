#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
A股基本面分析模块
"""

import json
import requests
from datetime import datetime
from typing import Dict, Any, Optional
from .quote import QuoteAnalyzer

class FundamentalAnalyzer:
    def __init__(self):
        self.quote_analyzer = QuoteAnalyzer()
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        })
    
    def _parse_eastmoney_fundamental(self, symbol: str) -> Optional[Dict[str, Any]]:
        """解析东方财富基本面数据"""
        try:
            # 转换symbol格式
            if symbol.startswith('sh'):
                em_symbol = f"1.{symbol[2:]}"
            elif symbol.startswith('sz'):
                em_symbol = f"0.{symbol[2:]}"
            else:
                em_symbol = symbol
            
            # 东方财富基本面API
            url = f'https://push2.eastmoney.com/api/qt/stock/get?secid={em_symbol}&fields=f58,f107,f57,f43,f169,f170,f152,f177,f111,f46,f60,f44,f45,f47,f260,f261,f279,f280,f19,f17,f15,f13,f11,f20,f18,f16,f14,f12,f39,f250,f251,f100,f101,f102,f103,f104,f105,f106'
            response = self.session.get(url, timeout=10)
            response.raise_for_status()
            
            data = response.json()
            if 'data' not in data or data['data'] is None:
                return None
            
            stock_data = data['data']
            
            # 获取基本信息
            stock_name = stock_data.get('f58', '')
            
            # 基本面指标
            eps = float(stock_data.get('f100', 0))  # 每股收益
            bps = float(stock_data.get('f101', 0))  # 每股净资产
            pe_ttm = float(stock_data.get('f102', 0))  # 市盈率(TTM)
            pe_ratio = float(stock_data.get('f17', 0))  # 市盈率
            pb_ratio = float(stock_data.get('f15', 0))  # 市净率
            roa = float(stock_data.get('f103', 0))  # 总资产收益率
            roe = float(stock_data.get('f104', 0))  # 净资产收益率
            gross_profit_rate = float(stock_data.get('f105', 0))  # 毛利率
            net_profit_rate = float(stock_data.get('f106', 0))  # 净利率
            
            # 财务数据
            total_assets = float(stock_data.get('f250', 0)) / 1e8  # 总资产(亿)
            circulating_market_cap = float(stock_data.get('f13', 0)) / 1e8  # 流通市值(亿)
            total_market_cap = float(stock_data.get('f11', 0)) / 1e8  # 总市值(亿)
            revenue = float(stock_data.get('f20', 0)) / 1e8  # 营业收入(亿)
            net_profit = float(stock_data.get('f18', 0)) / 1e8  # 净利润(亿)
            revenue_growth = float(stock_data.get('f14', 0))  # 营业收入增长率
            profit_growth = float(stock_data.get('f12', 0))  # 净利润增长率
            dividend_yield = float(stock_data.get('f39', 0))  # 股息率
            
            # 很有名（这里用市盈率的倒数作为知名度的一个简单指标）
            very_famous = 100.0 / pe_ratio if pe_ratio > 0 else 0.0
            
            return {
                "symbol": symbol,
                "stock_name": stock_name,
                "eps": round(eps, 2),
                "bps": round(bps, 2),
                "pe_ttm": round(pe_ttm, 2),
                "pe_ratio": round(pe_ratio, 2),
                "pb_ratio": round(pb_ratio, 2),
                "roa": round(roa, 2),
                "roe": round(roe, 2),
                "gross_profit_rate": round(gross_profit_rate, 2),
                "net_profit_rate": round(net_profit_rate, 2),
                "total_assets": round(total_assets, 2),
                "circulating_market_cap": round(circulating_market_cap, 2),
                "total_market_cap": round(total_market_cap, 2),
                "revenue": round(revenue, 2),
                "net_profit": round(net_profit, 2),
                "revenue_growth": round(revenue_growth, 2),
                "profit_growth": round(profit_growth, 2),
                "dividend_yield": round(dividend_yield, 2),
                "很有名": round(very_famous, 2)
            }
            
        except Exception as e:
            print(f"Error parsing EastMoney fundamental data for {symbol}: {e}")
            return None
    
    def fundamental_analysis(self, symbol: str) -> Dict[str, Any]:
        """执行基本面分析"""
        # 首先尝试获取基本面数据
        fundamental_data = self._parse_eastmoney_fundamental(symbol)
        
        if fundamental_data:
            return fundamental_data
        
        # 如果失败，返回基础结构
        quote_data = self.quote_analyzer.get_quote(symbol)
        stock_name = quote_data.get('stock_name', '')
        
        return {
            "symbol": symbol,
            "stock_name": stock_name,
            "eps": 0.0,
            "bps": 0.0,
            "pe_ttm": 0.0,
            "pe_ratio": 0.0,
            "pb_ratio": 0.0,
            "roa": 0.0,
            "roe": 0.0,
            "gross_profit_rate": 0.0,
            "net_profit_rate": 0.0,
            "total_assets": 0.0,
            "circulating_market_cap": 0.0,
            "total_market_cap": 0.0,
            "revenue": 0.0,
            "net_profit": 0.0,
            "revenue_growth": 0.0,
            "profit_growth": 0.0,
            "dividend_yield": 0.0,
            "很有名": 0.0
        }