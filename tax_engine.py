"""
Tax computation engine for TaxBot 2025
Implements New Tax Regime rules for FY 2024-25 and FY 2025-26
"""

from indian_formatter import format_indian_currency, format_indian_number

def get_tax_slabs(fy_ay):
    """
    Returns tax slabs based on Financial Year/Assessment Year
    """
    if fy_ay == "FY 2024-25 / AY 2025-26":
        return {
            "slabs": [
                (0, 300000, 0),      # 0-3L: 0%
                (300000, 700000, 0.05),  # 3-7L: 5%
                (700000, 1000000, 0.10), # 7-10L: 10%
                (1000000, 1200000, 0.15), # 10-12L: 15%
                (1200000, 1500000, 0.20), # 12-15L: 20%
                (1500000, float('inf'), 0.30) # 15L+: 30%
            ],
            "standard_deduction": 75000,
            "rebate_limit": 700000,
            "rebate_max": 25000,
            "advance_tax_threshold": 10000
        }
    elif fy_ay == "FY 2025-26 / AY 2026-27":
        return {
            "slabs": [
                (0, 400000, 0),      # 0-4L: 0% (Budget 2025 update)
                (400000, 700000, 0.05),  # 4-7L: 5%
                (700000, 1000000, 0.10), # 7-10L: 10%
                (1000000, 1200000, 0.15), # 10-12L: 15%
                (1200000, 1500000, 0.20), # 12-15L: 20%
                (1500000, float('inf'), 0.30) # 15L+: 30%
            ],
            "standard_deduction": 75000,
            "rebate_limit": 1200000,  # Increased to 12L
            "rebate_max": 60000,      # Increased to 60K
            "advance_tax_threshold": 10000
        }

def calculate_income_tax(taxable_income, fy_ay, age_group="Below 60"):
    """
    Calculate income tax based on New Tax Regime
    """
    config = get_tax_slabs(fy_ay)
    slabs = config["slabs"]
    
    tax = 0
    tax_breakdown = []
    
    for i, (lower, upper, rate) in enumerate(slabs):
        if taxable_income <= lower:
            break
            
        taxable_in_slab = min(taxable_income, upper) - lower
        slab_tax = taxable_in_slab * rate
        tax += slab_tax
        
        if slab_tax > 0:
            tax_breakdown.append({
                "slab": f"Rs. {format_indian_number(lower)} - Rs. {format_indian_number(upper)}" if upper != float('inf') else f"Rs. {format_indian_number(lower)}+",
                "rate": f"{rate*100:.0f}%",
                "taxable_amount": taxable_in_slab,
                "tax": slab_tax
            })
    
    return tax, tax_breakdown

def calculate_rebate_87a(gross_tax, taxable_income, fy_ay):
    """
    Calculate rebate under Section 87A
    """
    config = get_tax_slabs(fy_ay)
    
    if taxable_income <= config["rebate_limit"]:
        return min(gross_tax, config["rebate_max"])
    return 0

def calculate_cess_and_surcharge(tax_after_rebate, taxable_income):
    """
    Calculate Health & Education Cess (4%) and Surcharge
    """
    # Surcharge calculation
    surcharge = 0
    if taxable_income > 5000000:  # 50L+
        if taxable_income <= 10000000:  # 50L-1Cr
            surcharge = tax_after_rebate * 0.10
        elif taxable_income <= 20000000:  # 1Cr-2Cr
            surcharge = tax_after_rebate * 0.15
        elif taxable_income <= 50000000:  # 2Cr-5Cr
            surcharge = tax_after_rebate * 0.25
        else:  # 5Cr+
            surcharge = tax_after_rebate * 0.37
    
    # Health & Education Cess (4% on tax + surcharge)
    cess = (tax_after_rebate + surcharge) * 0.04
    
    return surcharge, cess

def calculate_capital_gains_tax(stcg, ltcg):
    """
    Calculate capital gains tax separately
    """
    # STCG: 15% (equity), 30% (other assets)
    # LTCG: 10% on gains > ₹1L (equity), 20% with indexation (other assets)
    
    stcg_tax = stcg * 0.15  # Assuming equity
    ltcg_tax = max(0, (ltcg - 100000)) * 0.10  # ₹1L exemption for equity LTCG
    
    return stcg_tax, ltcg_tax

def compute_total_tax_liability(income_details, fy_ay, employment_type):
    """
    Main function to compute total tax liability
    """
    # Calculate taxable income based on employment type
    taxable_income = 0
    
    if employment_type == "Salaried":
        gross_salary = income_details.get('basic_salary', 0) + \
                      income_details.get('hra', 0) + \
                      income_details.get('bonus', 0)
        
        # Standard deduction
        config = get_tax_slabs(fy_ay)
        taxable_income = max(0, gross_salary - config["standard_deduction"])
        
    elif employment_type == "Rental":
        rental_income = income_details.get('rent_received', 0) - \
                       income_details.get('municipal_tax', 0) - \
                       income_details.get('interest_paid', 0)
        taxable_income = max(0, rental_income)
        
    elif employment_type in ["Freelancer", "Business"]:
        taxable_income = income_details.get('net_profit', 0)
        
    elif employment_type == "Investor":
        other_income = income_details.get('dividends', 0) + \
                      income_details.get('interest_income', 0)
        taxable_income = other_income
    
    # Calculate regular income tax
    gross_tax, tax_breakdown = calculate_income_tax(taxable_income, fy_ay)
    
    # Calculate rebate
    rebate_87a = calculate_rebate_87a(gross_tax, taxable_income, fy_ay)
    tax_after_rebate = gross_tax - rebate_87a
    
    # Calculate surcharge and cess
    surcharge, cess = calculate_cess_and_surcharge(tax_after_rebate, taxable_income)
    
    # Calculate capital gains tax separately
    stcg_tax, ltcg_tax = calculate_capital_gains_tax(
        income_details.get('stcg', 0), 
        income_details.get('ltcg', 0)
    )
    
    # Total tax liability
    total_tax = tax_after_rebate + surcharge + cess + stcg_tax + ltcg_tax
    
    # Check advance tax requirement
    advance_tax_required = total_tax > get_tax_slabs(fy_ay)["advance_tax_threshold"]
    
    return {
        "taxable_income": taxable_income,
        "gross_tax": gross_tax,
        "rebate_87a": rebate_87a,
        "tax_after_rebate": tax_after_rebate,
        "surcharge": surcharge,
        "cess": cess,
        "stcg_tax": stcg_tax,
        "ltcg_tax": ltcg_tax,
        "total_tax": total_tax,
        "advance_tax_required": advance_tax_required,
        "tax_breakdown": tax_breakdown
    }
