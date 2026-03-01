#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
价值投资分析模块 - 基于《投资中最简单的事》和《股市进阶之道》
"""

import json
from typing import Dict, Any, List, Optional
from datetime import datetime

class ValueInvestingAnalyzer:
    """价值投资分析器 - 实现邱国鹭四要素和李杰能力圈理论"""
    
    def __init__(self):
        self.investment_principles = {
            "qiu_guolu": {
                "name": "邱国鹭四要素",
                "elements": ["估值", "品质", "时机", "仓位"]
            },
            "li_jie": {
                "name": "李杰能力圈理论",
                "elements": ["好生意", "好公司", "好价格"]
            }
        }
    
    def analyze_valuation(self, stock_data: Dict[str, Any]) -> Dict[str, Any]:
        """估值分析 - 判断是否便宜"""
        valuation_score = 0
        valuation_factors = {}
        
        # 市盈率分析
        pe_ratio = stock_data.get('p/e_ratio', 0)
        if pe_ratio > 0:
            if pe_ratio < 15:
                valuation_score += 25
                valuation_factors['pe_analysis'] = "低市盈率，估值合理"
            elif pe_ratio < 25:
                valuation_score += 15
                valuation_factors['pe_analysis'] = "市盈率适中"
            else:
                valuation_factors['pe_analysis'] = "高市盈率，估值偏高"
        
        # 市净率分析
        pb_ratio = stock_data.get('p/b_ratio', 0)
        if pb_ratio > 0:
            if pb_ratio < 1.5:
                valuation_score += 25
                valuation_factors['pb_analysis'] = "低市净率，资产价值被低估"
            elif pb_ratio < 3:
                valuation_score += 15
                valuation_factors['pb_analysis'] = "市净率适中"
            else:
                valuation_factors['pb_analysis'] = "高市净率，资产价值偏高"
        
        # 安全边际计算
        safety_margin = self._calculate_safety_margin(stock_data)
        valuation_factors['safety_margin'] = safety_margin
        
        if safety_margin > 0.3:
            valuation_score += 25
            valuation_factors['safety_margin_analysis'] = "安全边际充足"
        elif safety_margin > 0.15:
            valuation_score += 15
            valuation_factors['safety_margin_analysis'] = "安全边际适中"
        else:
            valuation_factors['safety_margin_analysis'] = "安全边际不足"
        
        return {
            "score": min(valuation_score, 100),
            "factors": valuation_factors,
            "recommendation": self._get_valuation_recommendation(valuation_score)
        }
    
    def analyze_quality(self, stock_data: Dict[str, Any]) -> Dict[str, Any]:
        """品质分析 - 判断公司是否优秀"""
        quality_score = 0
        quality_factors = {}
        
        # 护城河分析（需要更多数据，这里简化处理）
        moat_score = self._analyze_moat(stock_data)
        quality_score += moat_score
        quality_factors['moat_analysis'] = self._get_moat_description(moat_score)
        
        # ROE分析（需要基本面数据）
        roe = stock_data.get('roe', 0)
        if roe > 0:
            if roe > 15:
                quality_score += 20
                quality_factors['roe_analysis'] = "高ROE，盈利能力强"
            elif roe > 10:
                quality_score += 15
                quality_factors['roe_analysis'] = "ROE良好，盈利能力稳定"
            else:
                quality_factors['roe_analysis'] = "ROE偏低，盈利能力一般"
        
        # 现金流分析（需要基本面数据）
        free_cash_flow = stock_data.get('free_cash_flow', 0)
        if free_cash_flow > 0:
            quality_score += 20
            quality_factors['cash_flow_analysis'] = "自由现金流为正，财务健康"
        else:
            quality_factors['cash_flow_analysis'] = "自由现金流为负，需关注财务状况"
        
        # 负债率分析（需要基本面数据）
        debt_ratio = stock_data.get('debt_ratio', 0)
        if debt_ratio >= 0:
            if debt_ratio < 0.4:
                quality_score += 15
                quality_factors['debt_analysis'] = "低负债率，财务稳健"
            elif debt_ratio < 0.6:
                quality_score += 10
                quality_factors['debt_analysis'] = "负债率适中"
            else:
                quality_factors['debt_analysis'] = "高负债率，财务风险较高"
        
        return {
            "score": min(quality_score, 100),
            "factors": quality_factors,
            "recommendation": self._get_quality_recommendation(quality_score)
        }
    
    def analyze_timing(self, stock_data: Dict[str, Any], market_data: Dict[str, Any] = None) -> Dict[str, Any]:
        """时机分析 - 判断买入卖出时点"""
        timing_score = 50  # 默认中性
        timing_factors = {}
        
        # 市场情绪分析
        change_percent = stock_data.get('change_percent', 0)
        if change_percent < -5:
            timing_score += 20
            timing_factors['market_sentiment'] = "市场恐慌，可能是买入机会"
        elif change_percent > 5:
            timing_score -= 20
            timing_factors['market_sentiment'] = "市场过热，谨慎追高"
        else:
            timing_factors['market_sentiment'] = "市场情绪平稳"
        
        # 政策环境分析（需要外部数据）
        timing_factors['policy_environment'] = "需结合政策面分析"
        
        # 行业周期分析（需要行业数据）
        timing_factors['industry_cycle'] = "需结合行业周期判断"
        
        return {
            "score": max(0, min(timing_score, 100)),
            "factors": timing_factors,
            "recommendation": self._get_timing_recommendation(timing_score)
        }
    
    def analyze_position_sizing(self, valuation_score: int, quality_score: int, timing_score: int) -> Dict[str, Any]:
        """仓位管理建议"""
        total_score = (valuation_score * 0.4 + quality_score * 0.4 + timing_score * 0.2)
        
        if total_score >= 80:
            position = "重仓（60-80%）"
            recommendation = "优质标的，可重仓持有"
        elif total_score >= 60:
            position = "中仓（30-60%）"
            recommendation = "良好标的，可中等仓位"
        elif total_score >= 40:
            position = "轻仓（10-30%）"
            recommendation = "一般标的，建议轻仓"
        else:
            position = "观望（0-10%）"
            recommendation = "不建议投资，保持观望"
        
        return {
            "position": position,
            "recommendation": recommendation,
            "total_score": round(total_score, 2)
        }
    
    def analyze_business_model(self, stock_data: Dict[str, Any]) -> Dict[str, Any]:
        """商业模式分析 - 李杰的好生意理论"""
        business_score = 0
        business_factors = {}
        
        # 行业分析
        industry = stock_data.get('industry', '未知')
        business_factors['industry'] = industry
        
        # 商业模式可持续性
        business_model = stock_data.get('business_model', '未知')
        business_factors['business_model'] = business_model
        
        # 竞争格局
        competition = stock_data.get('competition', '未知')
        business_factors['competition'] = competition
        
        # 成长性
        growth_rate = stock_data.get('growth_rate', 0)
        if growth_rate > 0.2:
            business_score += 30
            business_factors['growth_analysis'] = "高成长性"
        elif growth_rate > 0.1:
            business_score += 20
            business_factors['growth_analysis'] = "良好成长性"
        else:
            business_factors['growth_analysis'] = "成长性一般"
        
        return {
            "score": min(business_score, 100),
            "factors": business_factors,
            "recommendation": self._get_business_recommendation(business_score)
        }
    
    def analyze_competitive_advantage(self, stock_data: Dict[str, Any]) -> Dict[str, Any]:
        """护城河分析"""
        moat_types = []
        
        # 品牌护城河
        if stock_data.get('brand_strength', 0) > 7:
            moat_types.append("品牌护城河")
        
        # 成本优势
        if stock_data.get('cost_advantage', 0) > 7:
            moat_types.append("成本优势护城河")
        
        # 网络效应
        if stock_data.get('network_effect', 0) > 7:
            moat_types.append("网络效应护城河")
        
        # 转换成本
        if stock_data.get('switching_cost', 0) > 7:
            moat_types.append("转换成本护城河")
        
        return {
            "moat_types": moat_types,
            "strength": len(moat_types),
            "analysis": f"识别到 {len(moat_types)} 种护城河类型: {', '.join(moat_types) if moat_types else '暂未识别到明显护城河'}"
        }
    
    def comprehensive_analysis(self, symbol: str, stock_data: Dict[str, Any]) -> Dict[str, Any]:
        """综合价值投资分析"""
        # 估值分析
        valuation_result = self.analyze_valuation(stock_data)
        
        # 品质分析
        quality_result = self.analyze_quality(stock_data)
        
        # 时机分析
        timing_result = self.analyze_timing(stock_data)
        
        # 仓位建议
        position_result = self.analyze_position_sizing(
            valuation_result['score'],
            quality_result['score'],
            timing_result['score']
        )
        
        # 商业模式分析
        business_result = self.analyze_business_model(stock_data)
        
        # 护城河分析
        moat_result = self.analyze_competitive_advantage(stock_data)
        
        return {
            "symbol": symbol,
            "stock_name": stock_data.get('stock_name', ''),
            "analysis_timestamp": datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            "investment_framework": {
                "qiu_guolu_four_elements": {
                    "valuation": valuation_result,
                    "quality": quality_result,
                    "timing": timing_result,
                    "position_sizing": position_result
                },
                "li_jie_three_good": {
                    "good_business": business_result,
                    "good_company": quality_result,
                    "good_price": valuation_result
                }
            },
            "overall_recommendation": position_result['recommendation'],
            "risk_warnings": self._identify_value_traps(stock_data),
            "investment_philosophy": "基于《投资中最简单的事》和《股市进阶之道》的价值投资理念"
        }
    
    def _calculate_safety_margin(self, stock_data: Dict[str, Any]) -> float:
        """计算安全边际"""
        # 简化计算：基于历史估值区间
        current_pe = stock_data.get('p/e_ratio', 0)
        if current_pe <= 0:
            return 0.0
        
        # 假设历史合理PE区间为10-20
        reasonable_pe_high = 20
        if current_pe < reasonable_pe_high:
            safety_margin = (reasonable_pe_high - current_pe) / reasonable_pe_high
            return max(0, min(safety_margin, 1))
        return 0.0
    
    def _analyze_moat(self, stock_data: Dict[str, Any]) -> int:
        """护城河分析评分"""
        moat_score = 0
        
        # 这里需要更多数据，暂时返回基础分数
        moat_score = 20  # 基础分数
        
        return moat_score
    
    def _get_moat_description(self, score: int) -> str:
        """获取护城河描述"""
        if score >= 80:
            return "强大护城河"
        elif score >= 60:
            return "良好护城河"
        elif score >= 40:
            return "一般护城河"
        else:
            return "护城河较弱"
    
    def _get_valuation_recommendation(self, score: int) -> str:
        """获取估值建议"""
        if score >= 80:
            return "估值极具吸引力，强烈建议关注"
        elif score >= 60:
            return "估值合理，可以考虑"
        elif score >= 40:
            return "估值偏高，谨慎对待"
        else:
            return "估值过高，建议回避"
    
    def _get_quality_recommendation(self, score: int) -> str:
        """获取品质建议"""
        if score >= 80:
            return "公司品质优秀，具备长期投资价值"
        elif score >= 60:
            return "公司品质良好，值得关注"
        elif score >= 40:
            return "公司品质一般，需谨慎评估"
        else:
            return "公司品质较差，建议回避"
    
    def _get_timing_recommendation(self, score: int) -> str:
        """获取时机建议"""
        if score >= 70:
            return "时机较好，可以考虑买入"
        elif score >= 50:
            return "时机中性，可持有观察"
        else:
            return "时机不佳，建议等待更好机会"
    
    def _get_business_recommendation(self, score: int) -> str:
        """获取商业模式建议"""
        if score >= 80:
            return "商业模式优秀，具备持续竞争优势"
        elif score >= 60:
            return "商业模式良好，有一定竞争优势"
        elif score >= 40:
            return "商业模式一般，需关注竞争变化"
        else:
            return "商业模式较弱，面临较大竞争压力"
    
    def _identify_value_traps(self, stock_data: Dict[str, Any]) -> List[str]:
        """识别价值陷阱"""
        warnings = []
        
        # 低PE但高负债
        pe_ratio = stock_data.get('p/e_ratio', 0)
        debt_ratio = stock_data.get('debt_ratio', 0)
        if pe_ratio > 0 and pe_ratio < 10 and debt_ratio > 0.7:
            warnings.append("低市盈率但高负债，可能存在价值陷阱")
        
        # 低PB但盈利持续下滑
        pb_ratio = stock_data.get('p/b_ratio', 0)
        profit_trend = stock_data.get('profit_trend', 'stable')
        if pb_ratio > 0 and pb_ratio < 1 and profit_trend == 'declining':
            warnings.append("低市净率但盈利持续下滑，需警惕价值陷阱")
        
        # 高股息但现金流紧张
        dividend_yield = stock_data.get('dividend_yield', 0)
        cash_flow = stock_data.get('free_cash_flow', 0)
        if dividend_yield > 5 and cash_flow < 0:
            warnings.append("高股息但现金流为负，股息可持续性存疑")
        
        if not warnings:
            warnings.append("未发现明显价值陷阱信号")
        
        return warnings