#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
A股实时分析技能主模块 - 基于邱国鹭《投资中最简单的事》和李杰《股市进阶之道》优化
"""

import json
import sys
import argparse
from datetime import datetime
import requests
import time
from typing import Dict, Any, Optional

# 导入各个功能模块
from .quote import get_realtime_quote
from .technical import get_technical_analysis
from .fundamental import get_fundamental_analysis
from .fund_flow import get_fund_flow
from .dragon_tiger import get_dragon_tiger_list
from .value_analysis import get_value_investing_analysis  # 新增价值投资分析

def main():
    """主函数"""
    parser = argparse.ArgumentParser(description='A股实时分析技能 - 基于价值投资理念优化')
    parser.add_argument('--action', type=str, required=True,
                       choices=['get_quote', 'technical_analysis', 'fundamental_analysis', 
                               'fund_flow', 'dragon_tiger_list', 'peer_comparison', 'value_investing_analysis'],
                       help='执行的操作类型')
    parser.add_argument('--symbol', type=str, help='股票代码 (如: sh600000, sz000001)')
    parser.add_argument('--indicator', type=str, help='技术指标 (逗号分隔，如: macd,rsi,kdj)')
    parser.add_argument('--period', type=str, help='资金流向周期 (逗号分隔，如: 5d,10d,20d)')
    parser.add_argument('--date', type=str, help='日期 (格式: YYYY-MM-DD)')
    
    args = parser.parse_args()
    
    try:
        if args.action == 'get_quote':
            if not args.symbol:
                raise ValueError("获取实时行情需要提供symbol参数")
            result = get_realtime_quote(args.symbol)
            
        elif args.action == 'technical_analysis':
            if not args.symbol:
                raise ValueError("技术分析需要提供symbol参数")
            indicators = args.indicator.split(',') if args.indicator else []
            result = get_technical_analysis(args.symbol, indicators)
            
        elif args.action == 'fundamental_analysis':
            if not args.symbol:
                raise ValueError("基本面分析需要提供symbol参数")
            result = get_fundamental_analysis(args.symbol)
            
        elif args.action == 'fund_flow':
            if not args.symbol:
                raise ValueError("资金流向分析需要提供symbol参数")
            periods = args.period.split(',') if args.period else []
            result = get_fund_flow(args.symbol, periods)
            
        elif args.action == 'dragon_tiger_list':
            date = args.date or datetime.now().strftime('%Y-%m-%d')
            result = get_dragon_tiger_list(date)
            
        elif args.action == 'peer_comparison':
            if not args.symbol:
                raise ValueError("同行对比需要提供symbol参数")
            # TODO: 实现同行对比功能
            result = {"error": "同行对比功能暂未实现"}
            
        elif args.action == 'value_investing_analysis':
            if not args.symbol:
                raise ValueError("价值投资分析需要提供symbol参数")
            result = get_value_investing_analysis(args.symbol)
            
        else:
            result = {"error": f"未知的操作类型: {args.action}"}
            
        # 输出标准JSON格式
        print(json.dumps(result, ensure_ascii=False, indent=2))
        
    except Exception as e:
        error_result = {
            "error": str(e),
            "action": args.action,
            "timestamp": datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        }
        print(json.dumps(error_result, ensure_ascii=False, indent=2))
        sys.exit(1)


if __name__ == "__main__":
    main()