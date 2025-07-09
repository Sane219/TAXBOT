"""
Smart tax tips module for TaxBot 2025
Provides context-aware tax advice based on user inputs
"""

import streamlit as st
from indian_formatter import format_indian_currency, format_indian_number

def get_smart_tips(income_details, tax_result, fy_ay, employment_type):
    """
    Generate smart tax tips based on user inputs and tax computation results
    """
    tips = []
    
    # Rebate eligibility tip
    if tax_result["rebate_87a"] > 0:
        tips.append({
            "icon": "💰",
            "title": "Section 87A Rebate Applied",
            "description": f"You're eligible for {format_indian_currency(tax_result['rebate_87a'])} rebate under Section 87A. This reduces your tax liability significantly!",
            "category": "rebate"
        })
    
    # HRA + Rent tip for salaried employees
    if employment_type == "Salaried":
        hra = income_details.get('hra', 0)
        rent_paid = income_details.get('rent_paid', 0)
        
        if hra > 0 and rent_paid > 0:
            hra_exemption = min(hra, rent_paid - (income_details.get('basic_salary', 0) * 0.1))
            if hra_exemption > 0:
                tips.append({
                    "icon": "🏠",
                    "title": "HRA Exemption Available",
                    "description": f"You can claim HRA exemption of approximately {format_indian_currency(hra_exemption)}. Ensure you have rent receipts and rental agreement.",
                    "category": "deduction"
                })
        elif hra > 0 and rent_paid == 0:
            tips.append({
                "icon": "⚠️",
                "title": "Missing Rent Information",
                "description": "You have HRA but haven't entered rent paid. HRA exemption is available if you pay rent.",
                "category": "missing_info"
            })
    
    # NPS investment tip
    if employment_type == "Salaried":
        employer_nps = income_details.get('employer_nps', 0)
        if employer_nps == 0:
            tips.append({
                "icon": "🏦",
                "title": "NPS Investment Opportunity",
                "description": "Consider investing in NPS for additional tax benefits up to Rs. 50,000 under Section 80CCD(1B).",
                "category": "investment"
            })
    
    # Capital gains threshold tip
    ltcg = income_details.get('ltcg', 0)
    if ltcg > 100000:
        tips.append({
            "icon": "📈",
            "title": "LTCG Tax Applicable",
            "description": f"Your LTCG of {format_indian_currency(ltcg)} exceeds Rs. 1,00,000. Tax of 10% applies on gains above Rs. 1L.",
            "category": "capital_gains"
        })
    elif ltcg > 0 and ltcg <= 100000:
        tips.append({
            "icon": "✅",
            "title": "LTCG Within Exemption Limit",
            "description": f"Your LTCG of {format_indian_currency(ltcg)} is within the Rs. 1,00,000 exemption limit. No tax applicable!",
            "category": "capital_gains"
        })
    
    # Advance tax warning
    if tax_result["advance_tax_required"]:
        tips.append({
            "icon": "⏰",
            "title": "Advance Tax Payment Required",
            "description": f"Your tax liability of {format_indian_currency(tax_result['total_tax'])} requires advance tax payment. Failure to pay may result in interest charges.",
            "category": "advance_tax"
        })
    
    # Presumptive taxation tip
    if employment_type in ["Freelancer", "Business"]:
        net_profit = income_details.get('net_profit', 0)
        if net_profit <= 5000000:  # Rs. 50L turnover limit for presumptive taxation
            tips.append({
                "icon": "📊",
                "title": "Presumptive Taxation Eligibility",
                "description": "You may be eligible for presumptive taxation scheme (Section 44AD/44ADA) for simplified tax calculation.",
                "category": "scheme"
            })
    
    # Standard deduction info
    if employment_type == "Salaried":
        tips.append({
            "icon": "📝",
            "title": "Standard Deduction Applied",
            "description": "Standard deduction of Rs. 75,000 has been applied to your salary income under the New Tax Regime.",
            "category": "deduction"
        })
    
    # New regime benefits
    if fy_ay == "FY 2025-26 / AY 2026-27":
        tips.append({
            "icon": "🎯",
            "title": "Budget 2025 Benefits",
            "description": "You're benefiting from increased tax-free limit (Rs. 4L), higher rebate limit (Rs. 12L), and maximum rebate (Rs. 60K).",
            "category": "regime"
        })
    
    return tips

def display_tips(tips):
    """
    Display smart tips in card format with simple styling
    """
    if not tips:
        st.info("No specific tips available based on your current inputs.")
        return
    
    st.subheader("🎯 Smart Tax Tips")
    
    # Group tips by category
    categories = {
        "rebate": "💰 Rebates & Savings",
        "deduction": "📝 Deductions",
        "investment": "🏦 Investment Opportunities",
        "capital_gains": "📈 Capital Gains",
        "advance_tax": "⏰ Tax Payments",
        "scheme": "📊 Tax Schemes",
        "regime": "🎯 New Tax Regime",
        "missing_info": "⚠️ Missing Information"
    }
    
    for category, category_title in categories.items():
        category_tips = [tip for tip in tips if tip["category"] == category]
        
        if category_tips:
            st.markdown(f"**{category_title}**")
            
            for tip in category_tips:
                # Use simple container with better styling
                with st.container():
                    st.markdown(f"""
                    <div style="
                        border: 1px solid #e0e0e0;
                        border-radius: 8px;
                        padding: 15px;
                        margin: 10px 0;
                        background-color: #f9f9f9;
                    ">
                        <div style="display: flex; align-items: center; margin-bottom: 8px;">
                            <span style="font-size: 20px; margin-right: 10px;">{tip['icon']}</span>
                            <strong>{tip['title']}</strong>
                        </div>
                        <p style="margin: 0; color: #666;">{tip['description']}</p>
                    </div>
                    """, unsafe_allow_html=True)

def get_tax_payment_guidance():
    """
    Provide guidance on tax payment and filing
    """
    st.subheader("💳 Tax Payment & Filing Guidance")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("""
        **📋 Step-by-step Guide to Challan 280 Payment:**
        1. Visit the Income Tax e-filing portal
        2. Go to 'e-Pay Tax' section
        3. Select 'Challan No./ITNS 280'
        4. Enter your PAN and select Assessment Year
        5. Choose payment method (Net Banking/Debit Card)
        6. Complete the payment process
        7. Download and save the challan receipt
        """)
    
    with col2:
        st.markdown("""
        **🔗 Important Links:**
        - [Income Tax e-filing Portal](https://www.incometax.gov.in/iec/foportal)
        - [Form 26AS](https://www.incometax.gov.in/iec/foportal/help/form-26as)
        - [Annual Information Statement (AIS)](https://www.incometax.gov.in/iec/foportal/help/ais)
        - [TDS Certificate Download](https://www.incometax.gov.in/iec/foportal/help/tds-certificates)
        """)

def get_document_checklist(employment_type):
    """
    Generate document checklist based on employment type
    """
    st.subheader("📄 Document Checklist")
    
    common_docs = [
        "PAN Card",
        "Aadhaar Card",
        "Bank Account Statements",
        "Form 26AS",
        "Annual Information Statement (AIS)"
    ]
    
    specific_docs = {
        "Salaried": [
            "Form 16 from employer",
            "Salary certificates",
            "HRA rent receipts and agreement",
            "Investment proofs (80C, 80D, etc.)",
            "Interest certificate from banks"
        ],
        "Freelancer": [
            "Professional income receipts",
            "Expense vouchers",
            "TDS certificates from clients",
            "Business registration documents"
        ],
        "Business": [
            "Business income statements",
            "Profit & Loss account",
            "Balance sheet",
            "Expense receipts",
            "GST returns"
        ],
        "Rental": [
            "Property documents",
            "Rent receipts",
            "Municipal tax receipts",
            "Home loan interest certificate",
            "Property tax receipts"
        ],
        "Investor": [
            "Share trading statements",
            "Dividend income certificates",
            "Interest income statements",
            "Capital gains statements",
            "Mutual fund statements"
        ]
    }
    
    all_docs = common_docs + specific_docs.get(employment_type, [])
    
    for doc in all_docs:
        st.markdown(f"☑️ {doc}")

def get_upcoming_deadlines():
    """
    Display upcoming tax deadlines
    """
    st.subheader("📅 Upcoming Tax Deadlines")
    
    deadlines = [
        {"date": "June 15, 2025", "description": "Q1 Advance Tax Payment (FY 2025-26)"},
        {"date": "July 31, 2025", "description": "ITR Filing Deadline (AY 2025-26)"},
        {"date": "September 15, 2025", "description": "Q2 Advance Tax Payment (FY 2025-26)"},
        {"date": "December 15, 2025", "description": "Q3 Advance Tax Payment (FY 2025-26)"},
        {"date": "March 15, 2026", "description": "Q4 Advance Tax Payment (FY 2025-26)"}
    ]
    
    for deadline in deadlines:
        st.markdown(f"📅 **{deadline['date']}**: {deadline['description']}")
