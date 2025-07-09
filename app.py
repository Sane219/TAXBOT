import streamlit as st
import json
import pandas as pd
import altair as alt

# Import additional components
from tax_engine import compute_total_tax_liability
from smart_tips import get_smart_tips, display_tips, get_tax_payment_guidance, get_document_checklist, get_upcoming_deadlines
from visualization import display_visualizations, offer_pdf_download
from indian_formatter import format_indian_currency, format_indian_number

# Helper function to format values for display
def format_value_display(value):
    if value > 0:
        return f"{format_indian_currency(value)}"
    return "Not entered"

# Improved layout
st.set_page_config(
    page_title="TaxBot 2025",
    layout="wide",
    initial_sidebar_state="expanded",
)

# Custom CSS styles
st.markdown("""
<style>
.main {
    background-color: #f5f5f5;
}
</style>
""", unsafe_allow_html=True)

# Initialize the Streamlit app
st.title("TaxBot 2025: Indian Income Tax Assistant")

# Initialize session state for form data
if 'form_submitted' not in st.session_state:
    st.session_state.form_submitted = False

# Form for personal information
with st.form(key='personal_info'):
    st.header("1. Personal Information")
    age_group = st.selectbox("Select Age Group", options=["Below 60", "60 and above", "80 and above"])
    residential_status = st.radio("Residential Status", options=["Resident", "Non-Resident"], help="Are you living in India?")
    fy_ay = st.selectbox("Financial Year / Assessment Year", options=["FY 2025-26 / AY 2026-27"], index=0, help="Choose the applicable financial year")
    employment_type = st.selectbox("Employment Type", options=["Salaried", "Freelancer", "Business", "Rental", "Investor", "Mixed"], help="Select your source of income")
    
    submit_info = st.form_submit_button(label='Submit Profile')
    
    if submit_info:
        st.session_state.form_submitted = True
        st.session_state.age_group = age_group
        st.session_state.residential_status = residential_status
        st.session_state.fy_ay = fy_ay
        st.session_state.employment_type = employment_type

# Added navigation
if st.session_state.form_submitted:
    tab_profile, tab_income, tab_taxation, tab_reports, tab_guidance = st.tabs(["Profile", "Income Details", "Tax Calculation", "Reports & Visualization", "Guidance"])

    with tab_profile:
        st.success("Profile information saved!")
        st.write(f"**Age Group:** {st.session_state.age_group}")
        st.write(f"**Residential Status:** {st.session_state.residential_status}")
        st.write(f"**Financial Year:** {st.session_state.fy_ay}")
        st.write(f"**Employment Type:** {st.session_state.employment_type}")

    with tab_income:
        # Initialize default values
        basic_salary = hra = pf = bonus = rent_paid = employer_nps = 0
        property_details = ""
        rent_received = municipal_tax = interest_paid = 0
        net_profit = expenses = 0
        presumptive_eligibility = False
        stcg = ltcg = dividends = interest_income = 0
        tds_paid = advance_tax_paid = 0
        
        if st.session_state.employment_type == "Salaried":
            st.subheader("Income Details: Salaried")
            col1, col2 = st.columns(2)
            with col1:
                basic_salary = st.number_input("Basic Salary", min_value=0, value=0, key="basic_salary")
                pf = st.number_input("Provident Fund Contribution", min_value=0, value=0, key="pf")
                bonus = st.number_input("Bonus", min_value=0, value=0, key="bonus")
            with col2:
                hra = st.number_input("HRA", min_value=0, value=0, key="hra")
                rent_paid = st.number_input("Rent Paid", min_value=0, value=0, key="rent_paid")
                employer_nps = st.number_input("Employer NPS Contribution", min_value=0, value=0, key="employer_nps")

        elif st.session_state.employment_type == "Rental":
            st.subheader("Income Details: Rental")
            col1, col2 = st.columns(2)
            with col1:
                property_details = st.text_input("Property Details", key="property_details")
                rent_received = st.number_input("Rent Received", min_value=0, value=0, key="rent_received")
            with col2:
                municipal_tax = st.number_input("Municipal Tax Paid", min_value=0, value=0, key="municipal_tax")
                interest_paid = st.number_input("Interest Paid on Home Loan", min_value=0, value=0, key="interest_paid")

        elif st.session_state.employment_type in ["Freelancer", "Business"]:
            st.subheader("Income Details: Freelance / Business")
            net_profit = st.number_input("Net Profit", min_value=0, value=0, key="net_profit")
            expenses = st.number_input("Expenses", min_value=0, value=0, key="expenses")
            presumptive_eligibility = st.checkbox("Eligible for Presumptive Taxation Scheme", key="presumptive")

        elif st.session_state.employment_type == "Investor":
            st.subheader("Income Details: Investor")
            col1, col2 = st.columns(2)
            with col1:
                stcg = st.number_input("Short Term Capital Gains (STCG)", min_value=0, value=0, key="stcg")
                ltcg = st.number_input("Long Term Capital Gains (LTCG)", min_value=0, value=0, key="ltcg")
            with col2:
                dividends = st.number_input("Dividends", min_value=0, value=0, key="dividends")
                interest_income = st.number_input("Interest Income", min_value=0, value=0, key="interest_income")

        # Optional inputs
        with st.expander("Optional Fields"):
            tds_paid = st.number_input("TDS Paid", min_value=0, value=0, key="tds_paid")
            advance_tax_paid = st.number_input("Advance Tax Paid", min_value=0, value=0, key="advance_tax_paid")
            
        # Store income details in session state
        st.session_state.income_details = {
            "basic_salary": basic_salary,
            "hra": hra,
            "pf": pf,
            "bonus": bonus,
            "rent_paid": rent_paid,
            "employer_nps": employer_nps,
            "rent_received": rent_received,
            "municipal_tax": municipal_tax,
            "interest_paid": interest_paid,
            "net_profit": net_profit,
            "expenses": expenses,
            "stcg": stcg,
            "ltcg": ltcg,
            "dividends": dividends,
            "interest_income": interest_income,
            "tds_paid": tds_paid,
            "advance_tax_paid": advance_tax_paid
        }

    with tab_taxation:
        if 'income_details' in st.session_state:
            if st.button("Calculate Tax", type="primary"):
                with st.spinner("Calculating tax..."):
                    try:
                        tax_result = compute_total_tax_liability(
                            st.session_state.income_details, 
                            st.session_state.fy_ay, 
                            st.session_state.employment_type
                        )
                        tips = get_smart_tips(
                            st.session_state.income_details, 
                            tax_result, 
                            st.session_state.fy_ay, 
                            st.session_state.employment_type
                        )
                        
                        st.session_state.tax_result = tax_result
                        st.session_state.tips = tips
                        
                        st.success("Tax calculation complete!")
                        
                        # Display results
                        display_visualizations(
                            st.session_state.income_details, 
                            tax_result, 
                            st.session_state.employment_type, 
                            st.session_state.fy_ay
                        )
                        display_tips(tips)
                        
                    except Exception as e:
                        st.error(f"Error in tax calculation: {str(e)}")
        else:
            st.info("Please enter your income details first.")

    with tab_reports:
        if 'tax_result' in st.session_state and 'tips' in st.session_state:
            offer_pdf_download(
                st.session_state.income_details, 
                st.session_state.tax_result, 
                st.session_state.tips, 
                st.session_state.employment_type, 
                st.session_state.fy_ay
            )
        else:
            st.info("Please calculate tax first to generate reports.")
            
    with tab_guidance:
        st.header("Tax Payment & Filing Guidance")
        get_tax_payment_guidance()
        
        st.header("Document Checklist")
        if 'employment_type' in st.session_state:
            get_document_checklist(st.session_state.employment_type)
        
        st.header("Important Deadlines")
        get_upcoming_deadlines()
        
else:
    st.info("Please submit your profile information to continue.")
