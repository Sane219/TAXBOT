"""
Visualization module for TaxBot 2025
Provides charts and PDF export functionality
"""

import streamlit as st
import pandas as pd
import altair as alt
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import io
from datetime import datetime
from indian_formatter import format_indian_currency, format_indian_number

def create_tax_breakdown_chart(tax_result):
    """
    Create a pie chart showing tax breakdown
    """
    components = []
    values = []
    
    if tax_result["tax_after_rebate"] > 0:
        components.append("Income Tax")
        values.append(tax_result["tax_after_rebate"])
    
    if tax_result["surcharge"] > 0:
        components.append("Surcharge")
        values.append(tax_result["surcharge"])
    
    if tax_result["cess"] > 0:
        components.append("Health & Education Cess")
        values.append(tax_result["cess"])
    
    if tax_result["stcg_tax"] > 0:
        components.append("STCG Tax")
        values.append(tax_result["stcg_tax"])
    
    if tax_result["ltcg_tax"] > 0:
        components.append("LTCG Tax")
        values.append(tax_result["ltcg_tax"])
    
    if not components:
        st.info("No tax liability to display.")
        return None
    
    fig = go.Figure(data=[go.Pie(
        labels=components,
        values=values,
        hole=0.3,
        hovertemplate='<b>%{label}</b><br>Amount: Rs. %{value:,.0f}<br>Percentage: %{percent}<extra></extra>'
    )])
    
    fig.update_layout(
        title="Tax Liability Breakdown",
        showlegend=True,
        height=400,
        margin=dict(t=60, b=20, l=20, r=20)
    )
    
    return fig

def create_income_composition_chart(income_details, employment_type):
    """
    Create a bar chart showing income composition
    """
    income_sources = []
    amounts = []
    
    if employment_type == "Salaried":
        if income_details.get('basic_salary', 0) > 0:
            income_sources.append("Basic Salary")
            amounts.append(income_details['basic_salary'])
        
        if income_details.get('hra', 0) > 0:
            income_sources.append("HRA")
            amounts.append(income_details['hra'])
        
        if income_details.get('bonus', 0) > 0:
            income_sources.append("Bonus")
            amounts.append(income_details['bonus'])
    
    elif employment_type == "Rental":
        if income_details.get('rent_received', 0) > 0:
            income_sources.append("Rent Received")
            amounts.append(income_details['rent_received'])
    
    elif employment_type in ["Freelancer", "Business"]:
        if income_details.get('net_profit', 0) > 0:
            income_sources.append("Net Profit")
            amounts.append(income_details['net_profit'])
    
    elif employment_type == "Investor":
        if income_details.get('dividends', 0) > 0:
            income_sources.append("Dividends")
            amounts.append(income_details['dividends'])
        
        if income_details.get('interest_income', 0) > 0:
            income_sources.append("Interest Income")
            amounts.append(income_details['interest_income'])
        
        if income_details.get('stcg', 0) > 0:
            income_sources.append("STCG")
            amounts.append(income_details['stcg'])
        
        if income_details.get('ltcg', 0) > 0:
            income_sources.append("LTCG")
            amounts.append(income_details['ltcg'])
    
    if not income_sources:
        st.info("No income data to display.")
        return None
    
    fig = go.Figure(data=[go.Bar(
        x=income_sources,
        y=amounts,
        marker_color='lightblue',
        hovertemplate='<b>%{x}</b><br>Amount: Rs. %{y:,.0f}<extra></extra>'
    )])
    
    fig.update_layout(
        title="Income Composition",
        xaxis_title="Income Sources",
        yaxis_title="Amount (Rs.)",
        height=400,
        margin=dict(t=60, b=60, l=60, r=20)
    )
    
    return fig

def create_tax_slab_visualization(tax_result, fy_ay):
    """
    Create a visualization showing tax slab utilization
    """
    if not tax_result["tax_breakdown"]:
        st.info("No tax slab data to display.")
        return None
    
    slabs = []
    rates = []
    amounts = []
    taxes = []
    
    for breakdown in tax_result["tax_breakdown"]:
        slabs.append(breakdown["slab"])
        rates.append(breakdown["rate"])
        amounts.append(breakdown["taxable_amount"])
        taxes.append(breakdown["tax"])
    
    # Create subplots
    fig = make_subplots(
        rows=1, cols=2,
        subplot_titles=('Taxable Amount by Slab', 'Tax by Slab'),
        specs=[[{"secondary_y": False}, {"secondary_y": False}]]
    )
    
    # Add taxable amount bars
    fig.add_trace(
        go.Bar(
            x=slabs,
            y=amounts,
            name="Taxable Amount",
            marker_color='lightgreen',
            hovertemplate='<b>%{x}</b><br>Taxable: Rs. %{y:,.0f}<extra></extra>'
        ),
        row=1, col=1
    )
    
    # Add tax bars
    fig.add_trace(
        go.Bar(
            x=slabs,
            y=taxes,
            name="Tax",
            marker_color='salmon',
            hovertemplate='<b>%{x}</b><br>Tax: Rs. %{y:,.0f}<extra></extra>'
        ),
        row=1, col=2
    )
    
    fig.update_layout(
        title=f"Tax Slab Utilization - {fy_ay}",
        height=500,
        showlegend=False,
        margin=dict(t=80, b=60, l=60, r=20)
    )
    
    return fig

def display_tax_summary_table(tax_result):
    """
    Display a formatted tax summary table
    """
    st.subheader("📊 Tax Calculation Summary")
    
    summary_data = {
        "Component": [
            "Taxable Income",
            "Gross Tax",
            "Section 87A Rebate",
            "Tax after Rebate",
            "Surcharge",
            "Health & Education Cess",
            "STCG Tax",
            "LTCG Tax",
            "Total Tax Liability"
        ],
        "Amount": [
            format_indian_currency(tax_result['taxable_income']),
            format_indian_currency(tax_result['gross_tax']),
            format_indian_currency(tax_result['rebate_87a']),
            format_indian_currency(tax_result['tax_after_rebate']),
            format_indian_currency(tax_result['surcharge']),
            format_indian_currency(tax_result['cess']),
            format_indian_currency(tax_result['stcg_tax']),
            format_indian_currency(tax_result['ltcg_tax']),
            format_indian_currency(tax_result['total_tax'])
        ]
    }
    
    df = pd.DataFrame(summary_data)
    st.table(df)

def generate_pdf_report(income_details, tax_result, tips, employment_type, fy_ay):
    """
    Generate PDF report (simplified version using HTML)
    """
    try:
        # Create HTML content for the report
        html_content = f"""
        <!DOCTYPE html>
        <html>
        <head>
            <title>TaxBot 2025 - Tax Report</title>
            <style>
                body {{ font-family: Arial, sans-serif; margin: 20px; }}
                .header {{ background-color: #f0f0f0; padding: 20px; text-align: center; }}
                .section {{ margin: 20px 0; }}
                .summary-table {{ width: 100%; border-collapse: collapse; }}
                .summary-table th, .summary-table td {{ border: 1px solid #ddd; padding: 8px; text-align: left; }}
                .summary-table th {{ background-color: #f2f2f2; }}
                .tip {{ background-color: #f9f9f9; padding: 10px; margin: 10px 0; border-left: 4px solid #007bff; }}
            </style>
        </head>
        <body>
            <div class="header">
                <h1>TaxBot 2025 - Tax Calculation Report</h1>
                <p>Generated on: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}</p>
                <p>Financial Year: {fy_ay}</p>
                <p>Employment Type: {employment_type}</p>
            </div>
            
            <div class="section">
                <h2>Tax Calculation Summary</h2>
                <table class="summary-table">
                    <tr><th>Component</th><th>Amount</th></tr>
                    <tr><td>Taxable Income</td><td>{format_indian_currency(tax_result['taxable_income'])}</td></tr>
                    <tr><td>Gross Tax</td><td>{format_indian_currency(tax_result['gross_tax'])}</td></tr>
                    <tr><td>Section 87A Rebate</td><td>{format_indian_currency(tax_result['rebate_87a'])}</td></tr>
                    <tr><td>Tax after Rebate</td><td>{format_indian_currency(tax_result['tax_after_rebate'])}</td></tr>
                    <tr><td>Surcharge</td><td>{format_indian_currency(tax_result['surcharge'])}</td></tr>
                    <tr><td>Health & Education Cess</td><td>{format_indian_currency(tax_result['cess'])}</td></tr>
                    <tr><td>STCG Tax</td><td>{format_indian_currency(tax_result['stcg_tax'])}</td></tr>
                    <tr><td>LTCG Tax</td><td>{format_indian_currency(tax_result['ltcg_tax'])}</td></tr>
                    <tr><td><strong>Total Tax Liability</strong></td><td><strong>{format_indian_currency(tax_result['total_tax'])}</strong></td></tr>
                </table>
            </div>
            
            <div class="section">
                <h2>Smart Tax Tips</h2>
        """
        
        for tip in tips:
            html_content += f"""
                <div class="tip">
                    <strong>{tip['icon']} {tip['title']}</strong>
                    <p>{tip['description']}</p>
                </div>
            """
        
        html_content += """
            </div>
            
            <div class="section">
                <h2>Disclaimer</h2>
                <p>This report is generated by TaxBot 2025 for informational purposes only. Please consult with a tax professional for official tax filing and advice.</p>
            </div>
        </body>
        </html>
        """
        
        return html_content
    
    except Exception as e:
        st.error(f"Error generating PDF report: {str(e)}")
        return None

def display_visualizations(income_details, tax_result, employment_type, fy_ay):
    """
    Display all visualizations
    """
    st.subheader("📈 Tax Visualizations")
    
    # Tax summary table
    display_tax_summary_table(tax_result)
    
    # Create two columns for charts
    col1, col2 = st.columns(2)
    
    with col1:
        # Tax breakdown pie chart
        tax_chart = create_tax_breakdown_chart(tax_result)
        if tax_chart:
            st.plotly_chart(tax_chart, use_container_width=True)
    
    with col2:
        # Income composition chart
        income_chart = create_income_composition_chart(income_details, employment_type)
        if income_chart:
            st.plotly_chart(income_chart, use_container_width=True)
    
    # Tax slab visualization (full width)
    slab_chart = create_tax_slab_visualization(tax_result, fy_ay)
    if slab_chart:
        st.plotly_chart(slab_chart, use_container_width=True)

def offer_pdf_download(income_details, tax_result, tips, employment_type, fy_ay):
    """
    Offer PDF download functionality
    """
    st.subheader("📄 Download Report")
    
    if st.button("Generate PDF Report"):
        html_content = generate_pdf_report(income_details, tax_result, tips, employment_type, fy_ay)
        
        if html_content:
            # Convert HTML to downloadable format
            st.download_button(
                label="Download Tax Report (HTML)",
                data=html_content,
                file_name=f"taxbot_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.html",
                mime="text/html"
            )
            
            st.success("Report generated successfully! Click the download button above to save it.")
        else:
            st.error("Failed to generate report. Please try again.")
