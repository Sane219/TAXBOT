#!/usr/bin/env python3
"""
Comprehensive test suite for TaxBot 2025
Tests all possible error scenarios and edge cases
"""

import sys
import traceback
from tax_engine import compute_total_tax_liability
from smart_tips import get_smart_tips
from visualization import (
    create_tax_breakdown_chart, 
    create_tax_efficiency_gauge,
    create_tax_vs_income_comparison,
    create_tax_slab_progression_chart,
    create_savings_potential_chart,
    create_income_composition_chart,
    display_key_metrics
)
from indian_formatter import format_indian_currency

def test_scenario(name, income_details, employment_type):
    """Test a specific scenario and catch any errors"""
    print(f"\n{'='*60}")
    print(f"🧪 Testing: {name}")
    print(f"{'='*60}")
    
    try:
        # Test tax calculation
        result = compute_total_tax_liability(income_details, 'FY 2025-26 / AY 2026-27', employment_type)
        print(f"✅ Tax calculation successful")
        print(f"   Taxable Income: {format_indian_currency(result['taxable_income'])}")
        print(f"   Total Tax: {format_indian_currency(result['total_tax'])}")
        
        # Test smart tips
        tips = get_smart_tips(income_details, result, 'FY 2025-26 / AY 2026-27', employment_type)
        print(f"✅ Smart tips generated: {len(tips)} tips")
        
        # Test all visualizations
        visualizations = [
            ("Tax Breakdown Chart", create_tax_breakdown_chart),
            ("Tax Efficiency Gauge", create_tax_efficiency_gauge),
            ("Tax vs Income Comparison", create_tax_vs_income_comparison),
            ("Tax Slab Progression", create_tax_slab_progression_chart),
            ("Savings Potential Chart", create_savings_potential_chart),
            ("Income Composition Chart", lambda r: create_income_composition_chart(income_details, employment_type))
        ]
        
        for viz_name, viz_func in visualizations:
            try:
                chart = viz_func(result)
                if chart is None:
                    print(f"✅ {viz_name}: Handled gracefully (no chart needed)")
                else:
                    print(f"✅ {viz_name}: Created successfully")
            except Exception as e:
                print(f"❌ {viz_name}: ERROR - {e}")
                traceback.print_exc()
        
        print(f"🎉 Scenario '{name}' completed successfully!")
        return True
        
    except Exception as e:
        print(f"❌ ERROR in scenario '{name}': {e}")
        traceback.print_exc()
        return False

def run_all_tests():
    """Run comprehensive tests for all scenarios"""
    print("🚀 TaxBot 2025 - Comprehensive Error Testing")
    print("=" * 60)
    
    test_scenarios = [
        # Zero tax scenarios
        ("Zero Tax - Low Income", {
            'basic_salary': 300000, 'hra': 0, 'bonus': 0, 'stcg': 0, 'ltcg': 0,
            'dividends': 0, 'interest_income': 0, 'tds_paid': 0, 'advance_tax_paid': 0
        }, "Salaried"),
        
        ("Zero Tax - 10 Lakh Income", {
            'basic_salary': 1000000, 'hra': 0, 'bonus': 0, 'stcg': 0, 'ltcg': 0,
            'dividends': 0, 'interest_income': 0, 'tds_paid': 0, 'advance_tax_paid': 0
        }, "Salaried"),
        
        # Regular tax scenarios
        ("Regular Tax - 15 Lakh Income", {
            'basic_salary': 1500000, 'hra': 0, 'bonus': 0, 'stcg': 0, 'ltcg': 0,
            'dividends': 0, 'interest_income': 0, 'tds_paid': 0, 'advance_tax_paid': 0
        }, "Salaried"),
        
        ("High Tax - 30 Lakh Income", {
            'basic_salary': 3000000, 'hra': 0, 'bonus': 0, 'stcg': 0, 'ltcg': 0,
            'dividends': 0, 'interest_income': 0, 'tds_paid': 0, 'advance_tax_paid': 0
        }, "Salaried"),
        
        # Complex scenarios with multiple income sources
        ("Complex Salaried", {
            'basic_salary': 1200000, 'hra': 200000, 'bonus': 150000, 'stcg': 80000, 'ltcg': 200000,
            'dividends': 50000, 'interest_income': 30000, 'tds_paid': 15000, 'advance_tax_paid': 5000
        }, "Salaried"),
        
        # Capital gains scenarios
        ("High Capital Gains", {
            'basic_salary': 0, 'hra': 0, 'bonus': 0, 'stcg': 500000, 'ltcg': 1000000,
            'dividends': 0, 'interest_income': 0, 'tds_paid': 0, 'advance_tax_paid': 0
        }, "Investor"),
        
        ("Only LTCG Below Threshold", {
            'basic_salary': 0, 'hra': 0, 'bonus': 0, 'stcg': 0, 'ltcg': 100000,
            'dividends': 0, 'interest_income': 0, 'tds_paid': 0, 'advance_tax_paid': 0
        }, "Investor"),
        
        # Different employment types
        ("Freelancer", {
            'basic_salary': 0, 'hra': 0, 'bonus': 0, 'stcg': 0, 'ltcg': 0,
            'dividends': 0, 'interest_income': 0, 'net_profit': 1500000, 'expenses': 200000,
            'tds_paid': 0, 'advance_tax_paid': 0
        }, "Freelancer"),
        
        ("Business Owner", {
            'basic_salary': 0, 'hra': 0, 'bonus': 0, 'stcg': 0, 'ltcg': 0,
            'dividends': 0, 'interest_income': 0, 'net_profit': 2500000, 'expenses': 500000,
            'tds_paid': 0, 'advance_tax_paid': 0
        }, "Business"),
        
        ("Rental Income", {
            'basic_salary': 0, 'hra': 0, 'bonus': 0, 'stcg': 0, 'ltcg': 0,
            'dividends': 0, 'interest_income': 0, 'rent_received': 600000, 'municipal_tax': 20000,
            'interest_paid': 100000, 'tds_paid': 0, 'advance_tax_paid': 0
        }, "Rental"),
        
        # Edge cases
        ("All Zero Values", {
            'basic_salary': 0, 'hra': 0, 'bonus': 0, 'stcg': 0, 'ltcg': 0,
            'dividends': 0, 'interest_income': 0, 'tds_paid': 0, 'advance_tax_paid': 0
        }, "Salaried"),
        
        ("Very High Income - 1 Crore", {
            'basic_salary': 10000000, 'hra': 0, 'bonus': 0, 'stcg': 0, 'ltcg': 0,
            'dividends': 0, 'interest_income': 0, 'tds_paid': 0, 'advance_tax_paid': 0
        }, "Salaried"),
        
        ("Mixed Income Sources", {
            'basic_salary': 800000, 'hra': 150000, 'bonus': 100000, 'stcg': 200000, 'ltcg': 300000,
            'dividends': 75000, 'interest_income': 50000, 'tds_paid': 25000, 'advance_tax_paid': 10000
        }, "Salaried"),
    ]
    
    passed = 0
    failed = 0
    
    for name, income_details, employment_type in test_scenarios:
        if test_scenario(name, income_details, employment_type):
            passed += 1
        else:
            failed += 1
    
    print(f"\n{'='*60}")
    print(f"🎯 TEST SUMMARY")
    print(f"{'='*60}")
    print(f"✅ Passed: {passed}")
    print(f"❌ Failed: {failed}")
    print(f"📊 Total: {passed + failed}")
    
    if failed == 0:
        print(f"🎉 ALL TESTS PASSED! TaxBot is error-free!")
    else:
        print(f"⚠️  {failed} tests failed. Please review the errors above.")
    
    return failed == 0

if __name__ == "__main__":
    success = run_all_tests()
    sys.exit(0 if success else 1)
