import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import numpy as np

# =====================================================
# PAGE CONFIGURATION
# =====================================================
st.set_page_config(
    page_title="Danone Amazon Insights",
    page_icon="🥛",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Danone color palette
DANONE_BLUE = "#1591EA"
DANONE_LIGHT_BLUE = "#00A9E0"
DANONE_ACCENT = "#E6F3FF"

# Custom CSS
st.markdown(f"""
<style>
    .main {{
        background: linear-gradient(135deg, {DANONE_ACCENT} 0%, #ffffff 100%);
    }}
    div[data-testid="stMetricValue"] {{
        font-size: 28px;
        color: {DANONE_BLUE};
    }}
    .upload-box {{
        border: 3px dashed {DANONE_LIGHT_BLUE};
        border-radius: 10px;
        padding: 30px;
        text-align: center;
        background-color: white;
    }}
    .big-font {{
        font-size: 1.2rem;
        line-height: 1.6;
    }}
</style>
""", unsafe_allow_html=True)

# =====================================================
# SIDEBAR NAVIGATION
# =====================================================
with st.sidebar:
    st.image("static/00_danone1.jpg", width=200)
    
    st.markdown("---")
    st.info("💡 **Tip:** Navigate through pages to explore different functionalities")
    
    st.markdown("---")
    st.markdown("### About")
    st.markdown("This dashboard analyzes Amazon product reviews to extract valuable insights and provide strategic recommendations.")

# =====================================================
# HEADER
# =====================================================
st.markdown(f"""
<div style='background: linear-gradient(135deg, {DANONE_BLUE} 0%, {DANONE_LIGHT_BLUE} 100%); 
            padding: 2rem; 
            border-radius: 10px; 
            margin-bottom: 2rem;
            box-shadow: 0 4px 6px rgba(0,0,0,0.1);'>
    <h1 style='color: white; margin: 0; font-size: 2.5rem;'>🥛 Costumer Opinion Analysis App</h1>
    <p style='color: white; margin: 0.5rem 0 0 0; opacity: 0.9; font-size: 1.1rem;'>
        A place to easily get insights from the costumers
    </p>
</div>
""", unsafe_allow_html=True)

# =====================================================
# PAGE 1: HOME / INTRODUCTION
# =====================================================
st.markdown("## Welcome to Danone Insights Dashboard")

st.markdown("""
<div class='big-font'>
This platform provides comprehensive analysis of customer reviews from Amazon to help Danone 
make data-driven decisions and improve product performance.
</div>
""", unsafe_allow_html=True)

st.markdown("---")

# Features section
col1, col2 = st.columns(2)

with col1:
    st.markdown(f"""
    <div style='background: linear-gradient(135deg, {DANONE_BLUE} 50%, {DANONE_LIGHT_BLUE} 100%)
                ; padding: 2rem; border-radius: 10px; box-shadow: 0 4px 6px rgba(0,0,0,0.1); 
                border-left: 5px solid #1591EA; height: 100%;'>
        <h3>📈 Insights & Recommendations</h3>
        <p><strong>What you'll find:</strong></p>
        <ul>
            <li><strong>Sentiment Analysis:</strong> Understand how customers feel about Danone products</li>
            <li><strong>Theme Detection:</strong> Identify the most discussed topics (taste, price, packaging, etc.)</li>
            <li><strong>Trend Analysis:</strong> Track sentiment evolution over time</li>
            <li><strong>Strategic Recommendations:</strong> Actionable insights based on customer feedback</li>
            <li><strong>Key Performance Indicators:</strong> Essential metrics at a glance</li>
        </ul>
        <p><strong>Use case:</strong> Perfect for presenting findings to stakeholders and understanding current product perception.</p>
    </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown(f"""
    <div style='background: background: linear-gradient(135deg, {DANONE_BLUE} 50%, {DANONE_LIGHT_BLUE} 100%)
                ; padding: 2rem; border-radius: 10px; box-shadow: 0 4px 6px rgba(0,0,0,0.1); 
                border-left: 5px solid {DANONE_LIGHT_BLUE}; height: 100%;'>
        <h3>🔍 Analyze New Dataset</h3>
        <p><strong>What you can do:</strong></p>
        <ul>
            <li><strong>Upload Excel Files:</strong> Simply drag and drop your .xlsx file</li>
            <li><strong>Filter by Brand (Marca):</strong> Analyze specific brands or all together</li>
            <li><strong>Automated Processing:</strong> Data cleaning and classification algorithms</li>
            <li><strong>Visual Results:</strong> Interactive charts and graphs</li>
            <li><strong>Export Results:</strong> Download processed data for further analysis</li>
        </ul>
        <p><strong>Use case:</strong> Ideal for analyzing new review batches and comparing different brands performance.</p>
    </div>
    """, unsafe_allow_html=True)

st.markdown("---")

# Quick stats
st.markdown("###  Platform Capabilities")

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.markdown(f"""
    <div style='background: white; padding: 1.5rem; border-radius: 10px; text-align: center; 
                box-shadow: 0 4px 6px rgba(0,0,0,0.1);'>
        <h2 style='color: {DANONE_BLUE}; margin: 0;'>6+</h2>
        <p style='color: #666; margin: 0.5rem 0 0 0;'>Themes Detected</p>
    </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown(f"""
    <div style='background: white; padding: 1.5rem; border-radius: 10px; text-align: center; 
                box-shadow: 0 4px 6px rgba(0,0,0,0.1);'>
        <h2 style='color: {DANONE_BLUE}; margin: 0;'>5</h2>
        <p style='color: #666; margin: 0.5rem 0 0 0;'>Sentiment Categories</p>
    </div>
    """, unsafe_allow_html=True)

with col3:
    st.markdown(f"""
    <div style='background: white; padding: 1.5rem; border-radius: 10px; text-align: center; 
                box-shadow: 0 4px 6px rgba(0,0,0,0.1);'>
        <h2 style='color: {DANONE_BLUE}; margin: 0;'>Excel</h2>
        <p style='color: #666; margin: 0.5rem 0 0 0;'>File Format Support</p>
    </div>
    """, unsafe_allow_html=True)

with col4:
    st.markdown(f"""
    <div style='background: white; padding: 1.5rem; border-radius: 10px; text-align: center; 
                box-shadow: 0 4px 6px rgba(0,0,0,0.1);'>
        <h2 style='color: {DANONE_BLUE}; margin: 0;'>Real-time</h2>
        <p style='color: #666; margin: 0.5rem 0 0 0;'>Analysis Processing</p>
    </div>
    """, unsafe_allow_html=True)

st.markdown("---")




    