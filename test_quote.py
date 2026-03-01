#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
测试实时行情功能
"""

import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))

from src.quote import QuoteAnalyzer

def test_quote():
    analyzer = QuoteAnalyzer()
    
    # 测试上证股票
    print("Testing 上证股票 (sh600000)...")
    quote_data = analyzer.get_quote('sh600000')
    print(json.dumps(quote_data, ensure_ascii=False, indent=2))
    
    # 测试深证股票
    print("\nTesting 深证股票 (sz000001)...")
    quote_data = analyzer.get_quote('sz000001')
    print(json.dumps(quote_data, ensure_ascii=False, indent=2))
    
    # 测试数字格式
    print("\nTesting 数字格式 (600000)...")
    quote_data = analyzer.get_quote('600000')
    print(json.dumps(quote_data, ensure_ascii=False, indent=2))

if __name__ == '__main__':
    import json
    test_quote()