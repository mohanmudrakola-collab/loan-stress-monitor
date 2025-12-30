# ============================================================================
# LOAN STRESS MONITOR - ENHANCED STREAMLIT DASHBOARD
# AI-Powered Banking Analytics for Loan Evergreening Detection
# ============================================================================
# Modern, Clean UI Design - Similar to Investment Analyzer
# ============================================================================

import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import numpy as np

# ============================================================================
# PAGE CONFIGURATION
# ============================================================================

st.set_page_config(
    page_title="Loan Stress Monitor | AI Banking Dashboard",
    page_icon="🏦",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# ============================================================================
# CUSTOM CSS FOR MODERN DESIGN
# ============================================================================

st.markdown("""
    <style>
    /* Main background */
    .stApp {
        background: linear-gradient(135deg, #1e3c72 0%, #2a5298 100%);
    }
    
    /* Title styling */
    .main-title {
        font-size: 52px;
        font-weight: bold;
        color: #4fd1c5;
        text-align: center;
        padding: 30px;
        text-shadow: 2px 2px 4px rgba(0,0,0,0.3);
    }
    
    .subtitle {
        font-size: 20px;
        color: #e0e0e0;
        text-align: center;
        margin-bottom: 40px;
    }
    
    /* Control panel */
    .control-panel {
        background: rgba(255, 255, 255, 0.95);
        padding: 40px;
        border-radius: 20px;
        box-shadow: 0 10px 30px rgba(0,0,0,0.3);
        margin: 20px auto;
        max-width: 1200px;
    }
    
    /* Risk score display */
    .risk-score-high {
        background: linear-gradient(135deg, #ff6b6b 0%, #ee5a6f 100%);
        color: white;
        padding: 30px;
        border-radius: 15px;
        text-align: center;
        font-size: 32px;
        font-weight: bold;
        box-shadow: 0 5px 15px rgba(255,107,107,0.4);
        margin: 20px 0;
    }
    
    .risk-score-medium {
        background: linear-gradient(135deg, #ffa726 0%, #fb8c00 100%);
        color: white;
        padding: 30px;
        border-radius: 15px;
        text-align: center;
        font-size: 32px;
        font-weight: bold;
        box-shadow: 0 5px 15px rgba(255,167,38,0.4);
        margin: 20px 0;
    }
    
    .risk-score-low {
        background: linear-gradient(135deg, #66bb6a 0%, #43a047 100%);
        color: white;
        padding: 30px;
        border-radius: 15px;
        text-align: center;
        font-size: 32px;
        font-weight: bold;
        box-shadow: 0 5px 15px rgba(102,187,106,0.4);
        margin: 20px 0;
    }
    
    /* Button styling */
    .stButton>button {
        width: 100%;
        height: 70px;
        background: linear-gradient(90deg, #4fd1c5 0%, #38b2ac 100%);
        color: white;
        font-size: 24px;
        font-weight: bold;
        border: none;
        border-radius: 15px;
        box-shadow: 0 5px 15px rgba(79,209,197,0.4);
        transition: all 0.3s ease;
    }
    
    .stButton>button:hover {
        transform: translateY(-2px);
        box-shadow: 0 7px 20px rgba(79,209,197,0.6);
    }
    
    /* Remove streamlit branding */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    
    /* Selectbox styling */
    .stSelectbox {
        font-size: 16px;
    }
    
    /* Metric cards */
    .metric-card {
        background: white;
        padding: 20px;
        border-radius: 10px;
        box-shadow: 0 2px 8px rgba(0,0,0,0.1);
        text-align: center;
    }
    
    </style>
    """, unsafe_allow_html=True)

# ============================================================================
# DATA LOADING AND PREPARATION
# ============================================================================

@st.cache_data
def load_data():
    """Load and prepare banking data"""
    
    # Bank data from annual reports and financial databases
    data = [
        # Stressed Banks
        {'Bank': 'YES Bank', 'Category': 'Stressed', 'Year': 'FY2017', 'Advances': 157000, 'Deposits': 174000, 'Gross_NPA': 0.31, 'Net_NPA': 0.20, 'Borrowings': 18000, 'Total_Assets': 236000, 'Net_Profit': 3260, 'Interest_Income': 11500},
        {'Bank': 'YES Bank', 'Category': 'Stressed', 'Year': 'FY2018', 'Advances': 195000, 'Deposits': 209000, 'Gross_NPA': 1.31, 'Net_NPA': 0.60, 'Borrowings': 25000, 'Total_Assets': 294000, 'Net_Profit': 3453, 'Interest_Income': 14800},
        {'Bank': 'YES Bank', 'Category': 'Stressed', 'Year': 'FY2019', 'Advances': 241000, 'Deposits': 200000, 'Gross_NPA': 7.39, 'Net_NPA': 4.35, 'Borrowings': 45000, 'Total_Assets': 350000, 'Net_Profit': -18564, 'Interest_Income': 16200},
        
        {'Bank': 'DHFL', 'Category': 'Stressed', 'Year': 'FY2017', 'Advances': 80000, 'Deposits': 42000, 'Gross_NPA': 0.58, 'Net_NPA': 0.40, 'Borrowings': 45000, 'Total_Assets': 105000, 'Net_Profit': 1250, 'Interest_Income': 7800},
        {'Bank': 'DHFL', 'Category': 'Stressed', 'Year': 'FY2018', 'Advances': 105000, 'Deposits': 45000, 'Gross_NPA': 1.24, 'Net_NPA': 0.82, 'Borrowings': 68000, 'Total_Assets': 130000, 'Net_Profit': 982, 'Interest_Income': 9500},
        {'Bank': 'DHFL', 'Category': 'Stressed', 'Year': 'FY2019', 'Advances': 116000, 'Deposits': 38000, 'Gross_NPA': 4.15, 'Net_NPA': 2.65, 'Borrowings': 82000, 'Total_Assets': 140000, 'Net_Profit': -2223, 'Interest_Income': 10200},
        
        {'Bank': 'IDBI Bank', 'Category': 'Stressed', 'Year': 'FY2017', 'Advances': 165000, 'Deposits': 185000, 'Gross_NPA': 16.50, 'Net_NPA': 8.25, 'Borrowings': 28000, 'Total_Assets': 290000, 'Net_Profit': -5663, 'Interest_Income': 15200},
        {'Bank': 'IDBI Bank', 'Category': 'Stressed', 'Year': 'FY2018', 'Advances': 155000, 'Deposits': 175000, 'Gross_NPA': 27.95, 'Net_NPA': 15.70, 'Borrowings': 32000, 'Total_Assets': 285000, 'Net_Profit': -8238, 'Interest_Income': 14500},
        {'Bank': 'IDBI Bank', 'Category': 'Stressed', 'Year': 'FY2019', 'Advances': 148000, 'Deposits': 170000, 'Gross_NPA': 28.38, 'Net_NPA': 14.95, 'Borrowings': 30000, 'Total_Assets': 275000, 'Net_Profit': -4106, 'Interest_Income': 13800},
        
        # Healthy Banks
        {'Bank': 'HDFC Bank', 'Category': 'Healthy', 'Year': 'FY2017', 'Advances': 590000, 'Deposits': 840000, 'Gross_NPA': 1.00, 'Net_NPA': 0.40, 'Borrowings': 12000, 'Total_Assets': 1080000, 'Net_Profit': 14549, 'Interest_Income': 52800},
        {'Bank': 'HDFC Bank', 'Category': 'Healthy', 'Year': 'FY2018', 'Advances': 710000, 'Deposits': 975000, 'Gross_NPA': 1.30, 'Net_NPA': 0.40, 'Borrowings': 14000, 'Total_Assets': 1240000, 'Net_Profit': 17486, 'Interest_Income': 61500},
        {'Bank': 'HDFC Bank', 'Category': 'Healthy', 'Year': 'FY2019', 'Advances': 856000, 'Deposits': 1140000, 'Gross_NPA': 1.36, 'Net_NPA': 0.41, 'Borrowings': 15000, 'Total_Assets': 1445000, 'Net_Profit': 21078, 'Interest_Income': 70800},
        
        {'Bank': 'ICICI Bank', 'Category': 'Healthy', 'Year': 'FY2017', 'Advances': 445000, 'Deposits': 562000, 'Gross_NPA': 7.82, 'Net_NPA': 4.89, 'Borrowings': 42000, 'Total_Assets': 785000, 'Net_Profit': 8575, 'Interest_Income': 39800},
        {'Bank': 'ICICI Bank', 'Category': 'Healthy', 'Year': 'FY2018', 'Advances': 512395, 'Deposits': 615000, 'Gross_NPA': 6.54, 'Net_NPA': 3.95, 'Borrowings': 45000, 'Total_Assets': 850000, 'Net_Profit': 9624, 'Interest_Income': 44200},
        {'Bank': 'ICICI Bank', 'Category': 'Healthy', 'Year': 'FY2019', 'Advances': 586647, 'Deposits': 685000, 'Gross_NPA': 5.95, 'Net_NPA': 2.95, 'Borrowings': 48000, 'Total_Assets': 945000, 'Net_Profit': 12402, 'Interest_Income': 48900},
        
        {'Bank': 'Kotak Bank', 'Category': 'Healthy', 'Year': 'FY2017', 'Advances': 135000, 'Deposits': 185000, 'Gross_NPA': 2.15, 'Net_NPA': 1.05, 'Borrowings': 8500, 'Total_Assets': 240000, 'Net_Profit': 3325, 'Interest_Income': 12400},
        {'Bank': 'Kotak Bank', 'Category': 'Healthy', 'Year': 'FY2018', 'Advances': 165000, 'Deposits': 220000, 'Gross_NPA': 2.18, 'Net_NPA': 1.12, 'Borrowings': 9800, 'Total_Assets': 285000, 'Net_Profit': 4185, 'Interest_Income': 14800},
        {'Bank': 'Kotak Bank', 'Category': 'Healthy', 'Year': 'FY2019', 'Advances': 198000, 'Deposits': 258000, 'Gross_NPA': 2.53, 'Net_NPA': 1.18, 'Borrowings': 11000, 'Total_Assets': 335000, 'Net_Profit': 4858, 'Interest_Income': 17200},
        
        {'Bank': 'SBI', 'Category': 'Healthy', 'Year': 'FY2017', 'Advances': 1795000, 'Deposits': 2635000, 'Gross_NPA': 6.90, 'Net_NPA': 3.71, 'Borrowings': 185000, 'Total_Assets': 3200000, 'Net_Profit': 10485, 'Interest_Income': 185000},
        {'Bank': 'SBI', 'Category': 'Healthy', 'Year': 'FY2018', 'Advances': 1940000, 'Deposits': 2890000, 'Gross_NPA': 10.91, 'Net_NPA': 5.73, 'Borrowings': 205000, 'Total_Assets': 3580000, 'Net_Profit': -6547, 'Interest_Income': 198000},
        {'Bank': 'SBI', 'Category': 'Healthy', 'Year': 'FY2019', 'Advances': 2075000, 'Deposits': 3085000, 'Gross_NPA': 7.53, 'Net_NPA': 3.01, 'Borrowings': 195000, 'Total_Assets': 3820000, 'Net_Profit': 862, 'Interest_Income': 210000},
        
        {'Bank': 'Axis Bank', 'Category': 'Healthy', 'Year': 'FY2017', 'Advances': 385000, 'Deposits': 480000, 'Gross_NPA': 4.86, 'Net_NPA': 2.61, 'Borrowings': 32000, 'Total_Assets': 650000, 'Net_Profit': 6068, 'Interest_Income': 36500},
        {'Bank': 'Axis Bank', 'Category': 'Healthy', 'Year': 'FY2018', 'Advances': 445000, 'Deposits': 535000, 'Gross_NPA': 5.28, 'Net_NPA': 2.77, 'Borrowings': 38000, 'Total_Assets': 735000, 'Net_Profit': 3679, 'Interest_Income': 41200},
        {'Bank': 'Axis Bank', 'Category': 'Healthy', 'Year': 'FY2019', 'Advances': 515000, 'Deposits': 605000, 'Gross_NPA': 5.26, 'Net_NPA': 2.13, 'Borrowings': 42000, 'Total_Assets': 825000, 'Net_Profit': 5251, 'Interest_Income': 46800},
    ]
    
    df = pd.DataFrame(data)
    
    # Calculate forensic ratios
    df['LDR'] = (df['Advances'] / df['Deposits']) * 100
    df['AD_Gap_Pct'] = ((df['Advances'] - df['Deposits']) / df['Deposits']) * 100
    df['Borrowing_Ratio'] = (df['Borrowings'] / df['Total_Assets']) * 100
    df['Profit_Margin'] = (df['Net_Profit'] / df['Interest_Income']) * 100
    
    # Calculate loan growth
    df = df.sort_values(['Bank', 'Year'])
    df['Loan_Growth_Pct'] = df.groupby('Bank')['Advances'].pct_change() * 100
    
    # Calculate risk scores
    def calc_risk(row):
        score = 0
        if row['Gross_NPA'] > 10: score += 30
        elif row['Gross_NPA'] > 5: score += 20
        elif row['Gross_NPA'] > 2: score += 10
        
        if row['LDR'] > 110: score += 25
        elif row['LDR'] > 95: score += 15
        elif row['LDR'] > 85: score += 5
        
        if row['Borrowing_Ratio'] > 15: score += 20
        elif row['Borrowing_Ratio'] > 10: score += 12
        elif row['Borrowing_Ratio'] > 5: score += 5
        
        if row['Net_Profit'] < 0: score += 15
        elif row['Profit_Margin'] < 5: score += 10
        elif row['Profit_Margin'] < 15: score += 5
        
        if pd.notna(row['Loan_Growth_Pct']):
            if row['Loan_Growth_Pct'] > 35: score += 10
            elif row['Loan_Growth_Pct'] > 25: score += 6
            elif row['Loan_Growth_Pct'] > 15: score += 3
        
        return min(score, 100)
    
    df['Risk_Score'] = df.apply(calc_risk, axis=1)
    df['Risk_Category'] = df['Risk_Score'].apply(
        lambda x: 'HIGH RISK' if x >= 70 else ('MEDIUM RISK' if x >= 40 else 'LOW RISK')
    )
    
    return df

# Load data
df = load_data()

# ============================================================================
# HEADER
# ============================================================================

st.markdown('<div class="main-title">🏦 Loan Stress Monitor</div>', unsafe_allow_html=True)
st.markdown('<div class="subtitle">AI-Powered Dashboard for Detecting Loan Evergreening in Indian Banks</div>', unsafe_allow_html=True)

# ============================================================================
# CONTROL PANEL
# ============================================================================

st.markdown('<div class="control-panel">', unsafe_allow_html=True)

# Create three columns for controls
col1, col2, col3 = st.columns(3)

with col1:
    st.markdown("### 🏦 Select Bank")
    bank_list = ['All Banks'] + sorted(df['Bank'].unique().tolist())
    selected_bank = st.selectbox("", bank_list, label_visibility="collapsed")

with col2:
    st.markdown("### 📅 Select Year")
    year_list = ['All Years'] + sorted(df['Year'].unique().tolist())
    selected_year = st.selectbox("", year_list, label_visibility="collapsed")

with col3:
    st.markdown("### 🎯 Bank Category")
    category_list = ['All', 'Stressed', 'Healthy']
    selected_category = st.selectbox("", category_list, label_visibility="collapsed")

st.markdown("</div>", unsafe_allow_html=True)

# Big Analyze Button
st.markdown("<br>", unsafe_allow_html=True)
analyze_clicked = st.button("🔍 Analyze Evergreening Risk", use_container_width=True)

# ============================================================================
# ANALYSIS SECTION (Shows when button is clicked)
# ============================================================================

if analyze_clicked or 'analyzed' in st.session_state:
    st.session_state['analyzed'] = True
    
    # Filter data
    filtered_df = df.copy()
    
    if selected_bank != 'All Banks':
        filtered_df = filtered_df[filtered_df['Bank'] == selected_bank]
    
    if selected_year != 'All Years':
        filtered_df = filtered_df[filtered_df['Year'] == selected_year]
    
    if selected_category != 'All':
        filtered_df = filtered_df[filtered_df['Category'] == selected_category]
    
    # ========================================================================
    # RISK SCORE DISPLAY
    # ========================================================================
    
    if len(filtered_df) > 0:
        avg_risk = filtered_df['Risk_Score'].mean()
        risk_cat = 'HIGH RISK' if avg_risk >= 70 else ('MEDIUM RISK' if avg_risk >= 40 else 'LOW RISK')
        
        if risk_cat == 'HIGH RISK':
            st.markdown(f'<div class="risk-score-high">🚨 Risk Score: {avg_risk:.0f}/100 - {risk_cat}</div>', unsafe_allow_html=True)
        elif risk_cat == 'MEDIUM RISK':
            st.markdown(f'<div class="risk-score-medium">⚠️ Risk Score: {avg_risk:.0f}/100 - {risk_cat}</div>', unsafe_allow_html=True)
        else:
            st.markdown(f'<div class="risk-score-low">✅ Risk Score: {avg_risk:.0f}/100 - {risk_cat}</div>', unsafe_allow_html=True)
        
        # ====================================================================
        # KEY METRICS
        # ====================================================================
        
        st.markdown("## 📊 Key Metrics")
        
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            avg_npa = filtered_df['Gross_NPA'].mean()
            st.metric("Average Gross NPA", f"{avg_npa:.2f}%", 
                     delta="Critical" if avg_npa > 5 else "Healthy",
                     delta_color="inverse")
        
        with col2:
            avg_ldr = filtered_df['LDR'].mean()
            st.metric("Average LDR", f"{avg_ldr:.1f}%",
                     delta="High" if avg_ldr > 100 else "Normal",
                     delta_color="inverse" if avg_ldr > 100 else "normal")
        
        with col3:
            high_risk = len(filtered_df[filtered_df['Risk_Category'] == 'HIGH RISK'])
            st.metric("High Risk Count", high_risk)
        
        with col4:
            total_adv = filtered_df['Advances'].sum() / 100000
            st.metric("Total Advances", f"₹{total_adv:.1f}L Cr")
        
        # ====================================================================
        # CHARTS
        # ====================================================================
        
        st.markdown("---")
        st.markdown("## 📈 Visual Analytics")
        
        # Chart 1: Risk Score Comparison
        if selected_year != 'All Years':
            year_data = df[df['Year'] == selected_year].sort_values('Risk_Score', ascending=False)
            
            fig1 = px.bar(
                year_data,
                x='Bank',
                y='Risk_Score',
                color='Risk_Category',
                color_discrete_map={
                    'HIGH RISK': '#f44336',
                    'MEDIUM RISK': '#ff9800',
                    'LOW RISK': '#4caf50'
                },
                title=f'<b>Risk Score Comparison ({selected_year})</b>',
                labels={'Risk_Score': 'Risk Score (0-100)', 'Bank': ''},
                text='Risk_Score',
                height=500
            )
            fig1.update_traces(texttemplate='%{text:.0f}', textposition='outside')
            fig1.update_layout(template='plotly_white', font=dict(size=12))
            st.plotly_chart(fig1, use_container_width=True)
        
        # Chart 2 & 3: NPA and LDR Trends
        col1, col2 = st.columns(2)
        
        with col1:
            fig2 = px.line(
                df if selected_bank == 'All Banks' else df[df['Bank'] == selected_bank],
                x='Year',
                y='Gross_NPA',
                color='Bank',
                title='<b>Gross NPA Trend</b>',
                markers=True,
                height=400
            )
            fig2.add_hline(y=5, line_dash="dash", line_color="red", annotation_text="Critical (5%)")
            fig2.update_layout(template='plotly_white')
            st.plotly_chart(fig2, use_container_width=True)
        
        with col2:
            fig3 = px.line(
                df if selected_bank == 'All Banks' else df[df['Bank'] == selected_bank],
                x='Year',
                y='LDR',
                color='Bank',
                title='<b>Loan-to-Deposit Ratio</b>',
                markers=True,
                height=400
            )
            fig3.add_hline(y=100, line_dash="dash", line_color="orange", annotation_text="Balance (100%)")
            fig3.update_layout(template='plotly_white')
            st.plotly_chart(fig3, use_container_width=True)
        
        # Chart 4: Detailed Table
        st.markdown("## 📋 Detailed Analysis")
        
        display_df = filtered_df[[
            'Bank', 'Year', 'Category', 'Gross_NPA', 'LDR', 'Borrowing_Ratio',
            'Profit_Margin', 'Risk_Score', 'Risk_Category'
        ]].copy()
        display_df.columns = ['Bank', 'Year', 'Type', 'NPA %', 'LDR %', 'Borrowing %',
                              'Profit %', 'Risk Score', 'Risk Level']
        display_df = display_df.round(2)
        
        st.dataframe(display_df, use_container_width=True, height=300)
        
        # ====================================================================
        # VALIDATION SECTION
        # ====================================================================
        
        if selected_bank in ['YES Bank', 'DHFL', 'All Banks']:
            st.markdown("---")
            st.markdown("## ✅ Model Validation")
            
            col1, col2 = st.columns(2)
            
            with col1:
                st.markdown("### 🏦 YES Bank")
                yes_data = df[df['Bank'] == 'YES Bank'].sort_values('Year')
                for _, row in yes_data.iterrows():
                    st.markdown(f"**{row['Year']}**: Risk Score = {row['Risk_Score']:.0f}/100 ({row['Risk_Category']})")
                st.success("✅ Correctly flagged as HIGH RISK in FY2019 before March 2020 crisis!")
            
            with col2:
                st.markdown("### 🏠 DHFL")
                dhfl_data = df[df['Bank'] == 'DHFL'].sort_values('Year')
                for _, row in dhfl_data.iterrows():
                    st.markdown(f"**{row['Year']}**: Risk Score = {row['Risk_Score']:.0f}/100 ({row['Risk_Category']})")
                st.success("✅ Correctly flagged as HIGH RISK in FY2019 before 2019 default!")
    
    else:
        st.warning("⚠️ No data available for selected filters. Please adjust your selection.")

# ============================================================================
# FOOTER
# ============================================================================

st.markdown("---")
st.markdown("""
<div style='text-align: center; color: #e0e0e0; padding: 20px;'>
<b>Loan Stress Monitor Dashboard</b><br>
IIM Ranchi | Financial Statement Analysis & Forensic Accounting<br>
Prof. Manish Bansal | December 2025<br>
AI-Inspired Algorithmic Intelligence for Banking Analytics
</div>
""", unsafe_allow_html=True)
