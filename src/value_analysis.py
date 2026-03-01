#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
价值投资分析模块 - 基于《投资中最简单的事》和《股市进阶之道》
"""

import json
from datetime import datetime
from typing import Dict, Any, Optional
from .fundamental import FundamentalAnalyzer
from .quote import QuoteAnalyzer

class ValueInvestingAnalyzer:
    def __init__(self):
        self.fundamental_analyzer = FundamentalAnalyzer()
        self.quote_analyzer = QuoteAnalyzer()
    
    def calculate_safety_margin(self, pe_ratio: float, pb_ratio: float, roe: float) -> float:
        """
        计算安全边际 - 邱国鹭的核心理念
        安全边际 = (内在价值 - 市场价格) / 内在价值
        这里用简化公式：基于PE、PB、ROE的综合评估
        """
        if pe_ratio <= 0 or pb_ratio <= 0 or roe <= 0:
            return 0.0
        
        # 简化内在价值计算：假设合理PE为15，合理PB为1.5
        reasonable_pe = 15.0
        reasonable_pb = 1.5
        
        # PE安全边际
        pe_safety = max(0, (reasonable_pe - pe_ratio) / reasonable_pe)
        
        # PB安全边际  
        pb_safety = max(0, (reasonable_pb - pb_ratio) / reasonable_pb)
        
        # ROE加成（高ROE公司可以有更高估值）
        roe_bonus = min(roe / 15.0, 1.0)  # ROE>15%为优秀
        
        # 综合安全边际
        safety_margin = (pe_safety + pb_safety) / 2 * (1 + roe_bonus * 0.2)
        
        return round(safety_margin, 2)
    
    def assess_moat(self, gross_profit_rate: float, net_profit_rate: float, 
                   revenue_growth: float, profit_growth: float) -> Dict[str, Any]:
        """
        评估护城河 - 邱国鹭和李杰都强调的核心概念
        """
        moat_score = 0
        moat_factors = []
        
        # 毛利率护城河（>40%为强护城河）
        if gross_profit_rate > 40:
            moat_score += 25
            moat_factors.append("高毛利率护城河")
        elif gross_profit_rate > 20:
            moat_score += 15
            moat_factors.append("中等毛利率护城河")
        
        # 净利率护城河（>15%为优秀）
        if net_profit_rate > 15:
            moat_score += 20
            moat_factors.append("高净利率护城河")
        elif net_profit_rate > 8:
            moat_score += 10
            moat_factors.append("良好净利率护城河")
        
        # 成长性护城河
        if revenue_growth > 15 and profit_growth > 15:
            moat_score += 20
            moat_factors.append("持续高成长护城河")
        elif revenue_growth > 5 and profit_growth > 5:
            moat_score += 10
            moat_factors.append("稳定成长护城河")
        
        # ROE护城河（>15%为优秀）
        # ROE会在主函数中传入
        
        moat_level = "弱"
        if moat_score >= 60:
            moat_level = "极强"
        elif moat_score >= 45:
            moat_level = "强"
        elif moat_score >= 30:
            moat_level = "中等"
        elif moat_score >= 15:
            moat_level = "弱"
            
        return {
            "moat_score": moat_score,
            "moat_level": moat_level,
            "moat_factors": moat_factors,
            "gross_profit_rate": round(gross_profit_rate, 2),
            "net_profit_rate": round(net_profit_rate, 2),
            "revenue_growth": round(revenue_growth, 2),
            "profit_growth": round(profit_growth, 2)
        }
    
    def identify_value_trap(self, pe_ratio: float, pb_ratio: float, roe: float, 
                          revenue_growth: float, profit_growth: float) -> Dict[str, Any]:
        """
        识别价值陷阱 - 李杰强调的重要概念
        """
        is_value_trap = False
        trap_reasons = []
        
        # 低PE但低ROE（可能是周期股底部或业务模式问题）
        if pe_ratio < 10 and roe < 8:
            is_value_trap = True
            trap_reasons.append("低PE低ROE组合")
        
        # 低PB但持续亏损或负增长
        if pb_ratio < 0.8 and (profit_growth < -5 or revenue_growth < -5):
            is_value_trap = True
            trap_reasons.append("低PB但负增长")
        
        # 高负债率（虽然当前代码没有负债数据，但可以标记）
        # 这里暂时不实现
        
        # 行业衰退（需要行业数据，暂时不实现）
        
        return {
            "is_value_trap": is_value_trap,
            "trap_reasons": trap_reasons,
            "pe_ratio": round(pe_ratio, 2),
            "pb_ratio": round(pb_ratio, 2),
            "roe": round(roe, 2),
            "revenue_growth": round(revenue_growth, 2),
            "profit_growth": round(profit_growth, 2)
        }
    
    def analyze_investment_timing(self, current_price: float, pe_ratio: float, 
                               pb_ratio: float, market_condition: str = "normal") -> Dict[str, Any]:
        """
        分析投资时机 - 邱国鹭四要素之一
        """
        timing_score = 0
        timing_advice = ""
        
        # 基于估值的时机判断
        if pe_ratio < 10 and pb_ratio < 1.0:
            timing_score = 90
            timing_advice = "极佳买入时机"
        elif pe_ratio < 15 and pb_ratio < 1.5:
            timing_score = 70
            timing_advice = "良好买入时机"
        elif pe_ratio < 20 and pb_ratio < 2.0:
            timing_score = 50
            timing_advice = "可考虑买入"
        elif pe_ratio > 30 or pb_ratio > 3.0:
            timing_score = 20
            timing_advice = "谨慎，估值偏高"
        else:
            timing_score = 40
            timing_advice = "观望"
        
        # 市场情绪调整（简化处理）
        if market_condition == "bear":
            timing_score = min(timing_score + 10, 100)
            timing_advice += " (熊市加成)"
        elif market_condition == "bull":
            timing_score = max(timing_score - 10, 0)
            timing_advice += " (牛市谨慎)"
        
        return {
            "timing_score": timing_score,
            "timing_advice": timing_advice,
            "current_price": round(current_price, 2),
            "pe_ratio": round(pe_ratio, 2),
            "pb_ratio": round(pb_ratio, 2),
            "market_condition": market_condition
        }
    
    def comprehensive_value_analysis(self, symbol: str) -> Dict[str, Any]:
        """
        综合价值投资分析
        """
        try:
            # 获取基本面数据
            fundamental_data = self.fundamental_analyzer.fundamental_analysis(symbol)
            quote_data = self.quote_analyzer.get_quote(symbol)
            
            # 提取关键指标
            pe_ratio = fundamental_data.get('pe_ratio', 0)
            pb_ratio = fundamental_data.get('pb_ratio', 0)
            roe = fundamental_data.get('roe', 0)
            gross_profit_rate = fundamental_data.get('gross_profit_rate', 0)
            net_profit_rate = fundamental_data.get('net_profit_rate', 0)
            revenue_growth = fundamental_data.get('revenue_growth', 0)
            profit_growth = fundamental_data.get('profit_growth', 0)
            current_price = quote_data.get('current_price', 0)
            
            # 计算安全边际
            safety_margin = self.calculate_safety_margin(pe_ratio, pb_ratio, roe)
            
            # 评估护城河
            moat_analysis = self.assess_moat(gross_profit_rate, net_profit_rate, 
                                           revenue_growth, profit_growth)
            
            # 识别价值陷阱
            value_trap_analysis = self.identify_value_trap(pe_ratio, pb_ratio, roe,
                                                        revenue_growth, profit_growth)
            
            # 分析投资时机
            timing_analysis = self.analyze_investment_timing(current_price, pe_ratio, pb_ratio)
            
            # 综合评分
            overall_score = 0
            score_factors = []
            
            # 安全边际得分 (0-25分)
            safety_score = min(safety_margin * 100, 25)
            overall_score += safety_score
            score_factors.append(f"安全边际: {safety_score:.1f}/25")
            
            # 护城河得分 (0-25分)
            moat_score = min(moat_analysis['moat_score'] * 0.25, 25)
            overall_score += moat_score
            score_factors.append(f"护城河: {moat_score:.1f}/25")
            
            # 价值陷阱扣分
            if value_trap_analysis['is_value_trap']:
                overall_score = max(overall_score - 20, 0)
                score_factors.append("价值陷阱: -20")
            
            # 时机得分 (0-25分)
            timing_score = timing_analysis['timing_score'] * 0.25
            overall_score += timing_score
            score_factors.append(f"投资时机: {timing_score:.1f}/25")
            
            # ROE质量得分 (0-25分)
            roe_score = min(roe / 4, 25)  # ROE>=100%得满分，实际很少见
            overall_score += roe_score
            score_factors.append(f"ROE质量: {roe_score:.1f}/25")
            
            investment_rating = "D"
            if overall_score >= 80:
                investment_rating = "A+"
            elif overall_score >= 70:
                investment_rating = "A"
            elif overall_score >= 60:
                investment_rating = "B+"
            elif overall_score >= 50:
                investment_rating = "B"
            elif overall_score >= 40:
                investment_rating = "C"
            else:
                investment_rating = "D"
            
            return {
                "symbol": symbol,
                "stock_name": fundamental_data.get('stock_name', ''),
                "analysis_timestamp": datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                "investment_rating": investment_rating,
                "overall_score": round(overall_score, 1),
                "score_breakdown": score_factors,
                "safety_margin": safety_margin,
                "moat_analysis": moat_analysis,
                "value_trap_analysis": value_trap_analysis,
                "timing_analysis": timing_analysis,
                "key_metrics": {
                    "pe_ratio": round(pe_ratio, 2),
                    "pb_ratio": round(pb_ratio, 2),
                    "roe": round(roe, 2),
                    "gross_profit_rate": round(gross_profit_rate, 2),
                    "net_profit_rate": round(net_profit_rate, 2),
                    "revenue_growth": round(revenue_growth, 2),
                    "profit_growth": round(profit_growth, 2),
                    "current_price": round(current_price, 2)
                }
            }
            
        except Exception as e:
            return {
                "error": f"价值投资分析失败: {str(e)}",
                "symbol": symbol,
                "analysis_timestamp": datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            }