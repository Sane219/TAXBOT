"""
Test script for TaxBot 2025
Tests all major components and functions
"""

import sys
import traceback

def test_imports():
    """Test if all required modules can be imported"""
    try:
        import streamlit as st
        import pandas as pd
        import altair as alt
        import plotly.graph_objects as go
        from datetime import datetime
        print("✅ All imports successful")
        return True
    except Exception as e:
        print(f" Import error: {e}")
        return False

def test_tax_engine():
    """Test the tax computation engine"""
    try:
        from tax_engine import compute_total_tax_liability, get_tax_slabs
        
        # Test tax slabs
        slabs_2024 = get_tax_slabs("FY 2024-25 / AY 2025-26")
        slabs_2025 = get_tax_slabs("FY 2025-26 / AY 2026-27")
        
        assert slabs_2024["rebate_limit"] == 700000
        assert slabs_2025["rebate_limit"] == 1200000
        
        # Test tax computation
        test_income = {
            "basic_salary": 600000,
            "hra": 200000,
            "pf": 0,
            "bonus": 50000,
            "rent_paid": 180000,
            "employer_nps": 0,
            "stcg": 0,
            "ltcg": 0,
            "dividends": 0,
            "interest_income": 0,
            "tds_paid": 0,
            "advance_tax_paid": 0
        }
        
        result = compute_total_tax_liability(test_income, "FY 2024-25 / AY 2025-26", "Salaried")
        assert result is not None
        assert "total_tax" in result
        assert "taxable_income" in result
        
        print("✅ Tax engine tests passed")
        return True
    except Exception as e:
        print(f" Tax engine error: {e}")
        traceback.print_exc()
        return False

def test_smart_tips():
    """Test the smart tips module"""
    try:
        from smart_tips import get_smart_tips
        
        test_income = {
            "basic_salary": 600000,
            "hra": 200000,
            "rent_paid": 180000,
            "ltcg": 150000,
            "stcg": 0,
            "dividends": 0,
            "interest_income": 0
        }
        
        test_tax_result = {
            "rebate_87a": 25000,
            "total_tax": 15000,
            "advance_tax_required": True
        }
        
        tips = get_smart_tips(test_income, test_tax_result, "FY 2024-25 / AY 2025-26", "Salaried")
        assert isinstance(tips, list)
        assert len(tips) > 0
        
        print("✅ Smart tips tests passed")
        return True
    except Exception as e:
        print(f" Smart tips error: {e}")
        traceback.print_exc()
        return False

def test_visualization():
    """Test the visualization module"""
    try:
        from visualization import create_tax_breakdown_chart, create_income_composition_chart
        
        test_tax_result = {
            "tax_after_rebate": 15000,
            "surcharge": 0,
            "cess": 600,
            "stcg_tax": 0,
            "ltcg_tax": 5000,
            "total_tax": 20600,
            "tax_breakdown": [
                {"slab": "₹3,00,000 - ₹7,00,000", "rate": "5%", "taxable_amount": 275000, "tax": 13750}
            ]
        }
        
        test_income = {
            "basic_salary": 600000,
            "hra": 200000,
            "bonus": 50000
        }
        
        # Test chart creation (returns None if no data, which is fine)
        tax_chart = create_tax_breakdown_chart(test_tax_result)
        income_chart = create_income_composition_chart(test_income, "Salaried")
        
        print("✅ Visualization tests passed")
        return True
    except Exception as e:
        print(f" Visualization error: {e}")
        traceback.print_exc()
        return False

def run_all_tests():
    """Run all tests"""
    print("🚀 Starting TaxBot 2025 tests...\n")
    
    tests = [
        ("Import Tests", test_imports),
        ("Tax Engine Tests", test_tax_engine),
        ("Smart Tips Tests", test_smart_tips),
        ("Visualization Tests", test_visualization)
    ]
    
    passed = 0
    total = len(tests)
    
    for test_name, test_func in tests:
        print(f"Running {test_name}...")
        if test_func():
            passed += 1
        print()
    
    print(f"📊 Test Results: {passed}/{total} tests passed")
    
    if passed == total:
        print("🎉 All tests passed! TaxBot 2025 is ready to use.")
    else:
        print("⚠️  Some tests failed. Please check the errors above.")
    
    return passed == total

if __name__ == "__main__":
    success = run_all_tests()
    sys.exit(0 if success else 1)
