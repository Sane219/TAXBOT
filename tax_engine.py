from indian_formatter import format_indian_currency, format_indian_number

def get_tax_slabs(fy_ay):
    """
    Returns tax slabs for FY 2025-26 / AY 2026-27
    """
    return {
        "slabs": [
            (0, 400000, 0),      # 0-4L: 0%
            (400000, 800000, 0.05),  # 4-8L: 5%
            (800000, 1200000, 0.10), # 8-12L: 10%
            (1200000, 1600000, 0.15), # 12-16L: 15%
            (1600000, 2000000, 0.20), # 16-20L: 20%
            (2000000, 2400000, 0.25), # 20-24L: 25%
            (2400000, float('inf'), 0.30) # 24L+: 30%
        ],
        "standard_deduction": 75000,
        "rebate_limit": 1200000,  # Up to 12L
        "rebate_max": 60000,      # Maximum 60K
        "advance_tax_threshold": 10000
    }

def calculate_income_tax(taxable_income, fy_ay, age_group="Below 60"):
    if not isinstance(taxable_income, (int, float)) or taxable_income < 0:
        raise ValueError("Taxable income must be a non-negative number")
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
    config = get_tax_slabs(fy_ay)
    if taxable_income <= config["rebate_limit"]:
        return min(gross_tax, config["rebate_max"])
    return 0

def calculate_cess_and_surcharge(tax_after_rebate, taxable_income):
    surcharge = 0
    if taxable_income > 5000000:
        if taxable_income <= 10000000:
            surcharge = tax_after_rebate * 0.10
        elif taxable_income <= 20000000:
            surcharge = tax_after_rebate * 0.15
        elif taxable_income <= 50000000:
            surcharge = tax_after_rebate * 0.25
        else:
            surcharge = tax_after_rebate * 0.37
    cess = (tax_after_rebate + surcharge) * 0.04
    return surcharge, cess

def calculate_capital_gains_tax(stcg, ltcg):
    """
    Calculate capital gains tax separately
    Updated for 2025-26: New capital gains tax rates
    """
    # STCG: 20% (equity and other assets) - Updated for 2025-26
    # LTCG: 12.5% on gains > ₹1.25L (equity), 20% with indexation (other assets)
    
    stcg_tax = stcg * 0.20  # Updated rate for 2025-26
    ltcg_tax = max(0, (ltcg - 125000)) * 0.125  # Updated exemption limit and rate for 2025-26
    
    return stcg_tax, ltcg_tax

def compute_total_tax_liability(income_details, fy_ay, employment_type):
    taxable_income = 0
    if employment_type == "Salaried":
        gross_salary = income_details.get('basic_salary', 0) + \
                       income_details.get('hra', 0) + \
                       income_details.get('bonus', 0)
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
    gross_tax, tax_breakdown = calculate_income_tax(taxable_income, fy_ay)
    rebate_87a = calculate_rebate_87a(gross_tax, taxable_income, fy_ay)
    tax_after_rebate = gross_tax - rebate_87a
    surcharge, cess = calculate_cess_and_surcharge(tax_after_rebate, taxable_income)
    stcg_tax, ltcg_tax = calculate_capital_gains_tax(
        income_details.get('stcg', 0),
        income_details.get('ltcg', 0)
    )
    total_tax = tax_after_rebate + surcharge + cess + stcg_tax + ltcg_tax
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