import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import numpy as np

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


st.markdown("## Alpro Analysis from the Costumer comments")


col1, col2 = st.columns(2)

with col1:
    st.markdown(f"""
    <div style='background: linear-gradient(135deg, {DANONE_BLUE} 0%, {DANONE_LIGHT_BLUE} 50%);
                padding: 2rem; border-radius: 10px; box-shadow: 0 4px 6px rgba(0,0,0,0.1);
                border-left: 5px solid #1591EA; height: 100%;'>
        <h3> Key Insights</h3>
        <ul>
            <li>The Alpro products from Danone receive many <strong>complaints about their price</strong>.</li>
            <li>Despite this, they still achieve <strong>very high ratings</strong>, which means customers love the products.</li>
            <li>Therefore, the dissatisfaction is <strong>not due to quality</strong> but due to a price that many consumers perceive as too high.</li>
            <li>The <strong>coconut flavour</strong> plays a major role: reviews show extremely positive comments and high scores specifically for coconut-based products.</li>
        </ul>
        <p>This reveals a strong product–market fit for coconut flavours, but with some pricing friction that affects customer perception.</p>
    </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown(f"""
    <div style='background: linear-gradient(135deg, {DANONE_LIGHT_BLUE} 50%, {DANONE_BLUE} 100%);
                padding: 2rem; border-radius: 10px; box-shadow: 0 4px 6px rgba(0,0,0,0.1);
                border-left: 5px solid #1591EA; height: 100%;'>
        <h3> Strategic Recommendations</h3>
        <ul>
            <li>Consider <strong>reducing the price</strong> of coconut products. Customers love them, but price sensitivity may limit purchases in some situations.</li>
            <li>Since coconut is a strong success driver, <strong>include samples of other flavours</strong> inside coconut-flavoured packs.</li>
        </ul>
        <p>This would strengthen the success of the coconut line while exposing customers to the broader, high-quality flavour range Alpro offers.</p>
    </div>
    """, unsafe_allow_html=True)