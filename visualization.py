"""
Enhanced Visualization module for TaxBot 2025
Provides interactive charts and comprehensive PDF export functionality
"""

import streamlit as st
import pandas as pd
import altair as alt
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import plotly.express as px
import numpy as np
import io
from datetime import datetime
from indian_formatter import format_indian_currency, format_indian_number
from tax_engine import get_tax_slabs

def create_tax_breakdown_chart(tax_result):
    """
    Create an enhanced and interactive pie chart showing tax breakdown
    """
    components = [
        "Income Tax", "Surcharge", "Health  Education Cess", "STCG Tax", "LTCG Tax"
    ]
    values = [
        tax_result["tax_after_rebate"],
        tax_result["surcharge"],
        tax_result["cess"],
        tax_result["stcg_tax"],
        tax_result["ltcg_tax"]
    ]
    
    # Filter zero values for a clean chart
    components, values = zip(*((c, v) for c, v in zip(components, values) if v > 0))
    
    if not components:
        st.info("No tax liability to display.")
        return None
    
    fig = px.pie(
        names=components,
        values=values,
        title="Enhanced Tax Liability Breakdown",
        hole=0.4,
        color_discrete_sequence=px.colors.sequential.RdBu
    )
    
    fig.update_traces(
        hovertemplate='be%{label}c/becbreAmount: Rs. %{value:,.0f}cbrePercentage: %{percent}cextraec/extrae',
        textposition='inside'
    )
    
    fig.update_layout(
        showlegend=True,
        height=450,
        margin=dict(t=30, b=20, l=20, r=20)
    )
    
    return fig

def create_tax_efficiency_gauge(tax_result):
    """
    Create a gauge chart showing tax efficiency
    """
    taxable_income = tax_result['taxable_income']
    total_tax = tax_result['total_tax']
    
    if taxable_income == 0:
        effective_tax_rate = 0
    else:
        effective_tax_rate = (total_tax / taxable_income) * 100
    
    fig = go.Figure(go.Indicator(
        mode="gauge+number+delta",
        value=effective_tax_rate,
        domain={'x': [0, 1], 'y': [0, 1]},
        title={'text': "Effective Tax Rate (%)"},
        delta={'reference': 20, 'relative': True},
        gauge={
            'axis': {'range': [None, 40]},
            'bar': {'color': "darkblue"},
            'steps': [
                {'range': [0, 10], 'color': "lightgray"},
                {'range': [10, 20], 'color': "yellow"},
                {'range': [20, 30], 'color': "orange"},
                {'range': [30, 40], 'color': "red"}
            ],
            'threshold': {
                'line': {'color': "red", 'width': 4},
                'thickness': 0.75,
                'value': 30
            }
        }
    ))
    
    fig.update_layout(
        height=350,
        margin=dict(l=20, r=20, t=40, b=20)
    )
    
    return fig

def create_tax_vs_income_comparison(tax_result):
    """
    Create a comparison chart between gross income and tax liability
    """
    taxable_income = tax_result['taxable_income']
    total_tax = tax_result['total_tax']
    net_income = taxable_income - total_tax
    
    categories = ['Gross Income', 'Tax Liability', 'Net Income']
    values = [taxable_income, total_tax, net_income]
    colors = ['#2E86AB', '#A23B72', '#F18F01']
    
    fig = go.Figure(data=[
        go.Bar(
            x=categories,
            y=values,
            marker_color=colors,
            text=[format_indian_currency(v) for v in values],
            textposition='auto',
            hovertemplate='<b>%{x}</b><br>Amount: Rs. %{y:,.0f}<extra></extra>'
        )
    ])
    
    fig.update_layout(
        title="Income vs Tax Liability Comparison",
        xaxis_title="Category",
        yaxis_title="Amount (Rs.)",
        height=400,
        showlegend=False
    )
    
    return fig

def create_tax_slab_progression_chart(tax_result):
    """
    Create a progressive tax slab visualization
    """
    if not tax_result["tax_breakdown"]:
        return None
    
    slabs = []
    rates = []
    cumulative_tax = 0
    cumulative_taxes = []
    
    for breakdown in tax_result["tax_breakdown"]:
        slabs.append(breakdown["slab"])
        rates.append(float(breakdown["rate"].replace('%', '')))
        cumulative_tax += breakdown["tax"]
        cumulative_taxes.append(cumulative_tax)
    
    # Create subplot with secondary y-axis
    fig = make_subplots(
        rows=1, cols=1,
        secondary_y=True,
        specs=[[{"secondary_y": True}]]
    )
    
    # Add bars for tax rates
    fig.add_trace(
        go.Bar(
            x=slabs,
            y=rates,
            name="Tax Rate (%)",
            marker_color='rgba(55, 83, 109, 0.7)',
            yaxis='y2'
        ),
        secondary_y=True
    )
    
    # Add line for cumulative tax
    fig.add_trace(
        go.Scatter(
            x=slabs,
            y=cumulative_taxes,
            mode='lines+markers',
            name='Cumulative Tax (Rs.)',
            line=dict(color='red', width=3),
            marker=dict(size=8)
        ),
        secondary_y=False
    )
    
    fig.update_layout(
        title="Tax Progression Across Slabs",
        height=450,
        hovermode='x unified'
    )
    
    fig.update_xaxes(title_text="Tax Slabs")
    fig.update_yaxes(title_text="Cumulative Tax (Rs.)", secondary_y=False)
    fig.update_yaxes(title_text="Tax Rate (%)", secondary_y=True)
    
    return fig

def create_savings_potential_chart(tax_result):
    """
    Create a chart showing potential savings opportunities
    """
    taxable_income = tax_result['taxable_income']
    current_tax = tax_result['total_tax']
    
    # Calculate potential savings with different deductions
    savings_scenarios = {
        'Current Tax': current_tax,
        'With 80C (₹1.5L)': max(0, current_tax - (150000 * 0.20)),  # Rough estimate
        'With NPS (₹50K)': max(0, current_tax - (50000 * 0.20)),
        'With Health Insurance': max(0, current_tax - (25000 * 0.20))
    }
    
    scenarios = list(savings_scenarios.keys())
    taxes = list(savings_scenarios.values())
    
    fig = go.Figure(data=[
        go.Bar(
            x=scenarios,
            y=taxes,
            marker_color=['#FF6B6B', '#4ECDC4', '#45B7D1', '#96CEB4'],
            text=[format_indian_currency(t) for t in taxes],
            textposition='auto',
            hovertemplate='<b>%{x}</b><br>Tax: Rs. %{y:,.0f}<extra></extra>'
        )
    ])
    
    fig.update_layout(
        title="Tax Savings Potential with Different Deductions",
        xaxis_title="Scenarios",
        yaxis_title="Tax Amount (Rs.)",
        height=400,
        showlegend=False
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

def display_key_metrics(tax_result):
    """
    Display key tax metrics in a dashboard format
    """
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric(
            label="Total Tax Liability",
            value=format_indian_currency(tax_result['total_tax']),
            delta=f"-{format_indian_currency(tax_result['rebate_87a'])}" if tax_result['rebate_87a'] > 0 else None,
            delta_color="inverse"
        )
    
    with col2:
        effective_rate = (tax_result['total_tax'] / tax_result['taxable_income'] * 100) if tax_result['taxable_income'] > 0 else 0
        st.metric(
            label="Effective Tax Rate",
            value=f"{effective_rate:.2f}%",
            delta=f"{'Below 30%' if effective_rate < 30 else 'Above 30%'}",
            delta_color="normal" if effective_rate < 30 else "inverse"
        )
    
    with col3:
        net_income = tax_result['taxable_income'] - tax_result['total_tax']
        st.metric(
            label="Net Take-home",
            value=format_indian_currency(net_income),
            delta=f"{(net_income/tax_result['taxable_income']*100):.1f}% of gross" if tax_result['taxable_income'] > 0 else "0%"
        )
    
    with col4:
        st.metric(
            label="Advance Tax Required",
            value="Yes" if tax_result['advance_tax_required'] else "No",
            delta="Due in quarterly installments" if tax_result['advance_tax_required'] else "Annual filing sufficient"
        )

def display_visualizations(income_details, tax_result, employment_type, fy_ay):
    """
    Display enhanced visualizations for tax insights
    """
    st.subheader("📈 Comprehensive Tax Visualizations")
    
    # Display key metrics first
    display_key_metrics(tax_result)
    
    st.divider()
    
    # Tax summary table
    display_tax_summary_table(tax_result)
    
    # Create a three-column layout
    col1, col2, col3 = st.columns(3)
    
    with col1:
        tax_chart = create_tax_breakdown_chart(tax_result)
        if tax_chart:
            st.plotly_chart(tax_chart, use_container_width=True)
        efficiency_gauge = create_tax_efficiency_gauge(tax_result)
        if efficiency_gauge:
            st.plotly_chart(efficiency_gauge, use_container_width=True)
    
    with col2:
        income_chart = create_income_composition_chart(income_details, employment_type)
        if income_chart:
            st.plotly_chart(income_chart, use_container_width=True)
        tax_vs_income = create_tax_vs_income_comparison(tax_result)
        if tax_vs_income:
            st.plotly_chart(tax_vs_income, use_container_width=True)
    
    with col3:
        savings_potential_chart = create_savings_potential_chart(tax_result)
        if savings_potential_chart:
            st.plotly_chart(savings_potential_chart, use_container_width=True)
        slab_progression_chart = create_tax_slab_progression_chart(tax_result)
        if slab_progression_chart:
            st.plotly_chart(slab_progression_chart, use_container_width=True)

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
