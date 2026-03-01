#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
A股资金流向分析模块
"""

import json
import requests
from datetime import datetime
from typing import Dict, Any, Optional
from .quote import QuoteAnalyzer

class FundFlowAnalyzer:
    def __init__(self):
        self.quote_analyzer = QuoteAnalyzer()
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        })
    
    def _parse_eastmoney_fund_flow(self, symbol: str, period: str = 'latest') -> Optional[Dict[str, Any]]:
        """解析东方财富资金流向数据"""
        try:
            # 转换symbol格式
            if symbol.startswith('sh'):
                em_symbol = f"1.{symbol[2:]}"
            elif symbol.startswith('sz'):
                em_symbol = f"0.{symbol[2:]}"
            else:
                em_symbol = symbol
            
            # 东方财富资金流向API
            url = f'https://push2.eastmoney.com/api/qt/stock/fflow/daykline?secid={em_symbol}&lmt=20'
            response = self.session.get(url, timeout=10)
            response.raise_for_status()
            
            data = response.json()
            if 'data' not in data or 'klines' not in data['data']:
                return None
            
            klines = data['data']['klines']
            if not klines:
                return None
            
            # 解析最新的资金流向数据
            latest_data = klines[-1].split(',')
            if len(latest_data) < 12:
                return None
            
            # 提取资金流向数据（单位：万元）
            main_net = float(latest_data[1]) if latest_data[1] else 0.0
            super_net = float(latest_data[2]) if latest_data[2] else 0.0
            big_net = float(latest_data[3]) if latest_data[3] else 0.0
            middle_net = float(latest_data[4]) if latest_data[4] else 0.0
            small_net = float(latest_data[5]) if latest_data[5] else 0.0
            
            fund_flow_data = {
                "main_net": round(main_net, 2),
                "super_net": round(super_net, 2),
                "big_net": round(big_net, 2),
                "middle_net": round(middle_net, 2),
                "small_net": round(small_net, 2)
            }
            
            if period == 'latest':
                return {"latest": fund_flow_data}
            
            # 计算多日累计数据
            def calculate_period_sum(days):
                if len(klines) < days:
                    days = len(klines)
                
                period_sum = {
                    "main_net": 0.0,
                    "super_net": 0.0,
                    "big_net": 0.0,
                    "middle_net": 0.0,
                    "small_net": 0.0
                }
                
                for i in range(max(0, len(klines) - days), len(klines)):
                    line_data = klines[i].split(',')
                    if len(line_data) >= 6:
                        period_sum["main_net"] += float(line_data[1]) if line_data[1] else 0.0
                        period_sum["super_net"] += float(line_data[2]) if line_data[2] else 0.0
                        period_sum["big_net"] += float(line_data[3]) if line_data[3] else 0.0
                        period_sum["middle_net"] += float(line_data[4]) if line_data[4] else 0.0
                        period_sum["small_net"] += float(line_data[5]) if line_data[5] else 0.0
                
                return {k: round(v, 2) for k, v in period_sum.items()}
            
            result = {"latest": fund_flow_data}
            
            if '5d' in period or period == 'all':
                result["5_days"] = calculate_period_sum(5)
            
            if '10d' in period or period == 'all':
                result["10_days"] = calculate_period_sum(10)
            
            if '20d' in period or period == 'all':
                result["20_days"] = calculate_period_sum(20)
            
            return result
            
        except Exception as e:
            print(f"Error parsing EastMoney fund flow data for {symbol}: {e}")
            return None
    
    def _generate_signal(self, fund_flow: Dict[str, Any]) -> str:
        """生成资金流向信号"""
        latest = fund_flow.get('latest', {})
        main_net = latest.get('main_net', 0)
        
        if main_net > 0:
            return "主力资金流入"
        elif main_net < 0:
            return "主力资金流出"
        else:
            return "资金流向平衡"
    
    def fund_flow_analysis(self, symbol: str, period: str = 'latest') -> Dict[str, Any]:
        """执行资金流向分析"""
        # 获取当前行情
        quote_data = self.quote_analyzer.get_quote(symbol)
        current_price = quote_data.get('current_price', 0)
        stock_name = quote_data.get('stock_name', '')
        change_percent = quote_data.get('change_percent', 0)
        
        # 获取资金流向数据
        fund_flow_data = self._parse_eastmoney_fund_flow(symbol, period)
        
        if not fund_flow_data:
            # 返回空数据结构
            empty_flow = {
                "main_net": 0.0,
                "super_net": 0.0,
                "big_net": 0.0,
                "middle_net": 0.0,
                "small_net": 0.0
            }
            
            fund_flow = {"latest": empty_flow}
            if '5d' in period or period == 'all':
                fund_flow["5_days"] = empty_flow.copy()
            if '10d' in period or period == 'all':
                fund_flow["10_days"] = empty_flow.copy()
            if '20d' in period or period == 'all':
                fund_flow["20_days"] = empty_flow.copy()
        else:
            fund_flow = fund_flow_data
        
        current_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        signal = self._generate_signal(fund_flow)
        
        return {
            "symbol": symbol,
            "stock_name": stock_name,
            "current_price": round(current_price, 2),
            "change_percent": round(change_percent, 2),
            "time": current_time,
            "fund_flow": fund_flow,
            "signal": signal
        }