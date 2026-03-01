import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go

# Page Configuration
st.set_page_config(
    page_title="DataInsight Dashboard",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded",
)

# Custom CSS for Premium Look
st.markdown("""
    <style>
    .main {
        background-color: #0e1117;
    }
    .stMetric {
        background-color: #1f2937;
        padding: 15px;
        border-radius: 10px;
        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1);
    }
    </style>
    """, unsafe_allow_html=True)

# Generate Mock Data
@st.cache_data
def load_data():
    dates = pd.date_range(start="2024-01-01", end="2024-12-31", freq="D")
    data = pd.DataFrame({
        "Date": dates,
        "Sales": np.random.randint(200, 1000, size=len(dates)),
        "Users": np.random.randint(50, 300, size=len(dates)),
        "Revenue": np.random.uniform(5000, 15000, size=len(dates)),
        "Region": np.random.choice(["North", "South", "East", "West"], size=len(dates))
    })
    return data

df = load_data()

# Sidebar
st.sidebar.title("Navigation")
region_filter = st.sidebar.multiselect("Select Region", options=df["Region"].unique(), default=df["Region"].unique())
date_range = st.sidebar.date_input("Date Range", [df["Date"].min(), df["Date"].max()])

# Filter Data
filtered_df = df[(df["Region"].isin(region_filter)) & 
                 (df["Date"] >= pd.to_datetime(date_range[0])) & 
                 (df["Date"] <= pd.to_datetime(date_range[1]))]

# Top Metrics
st.title("📊 DataInsight Dashboard")
st.markdown("---")

col1, col2, col3, col4 = st.columns(4)
with col1:
    st.metric("Total Sales", f"{filtered_df['Sales'].sum():,}")
with col2:
    st.metric("Total Revenue", f"${filtered_df['Revenue'].sum():,.2f}")
with col3:
    st.metric("Avg Users", f"{int(filtered_df['Users'].mean())}")
with col4:
    st.metric("Growth", "+12.5%", delta_color="normal")

# Visualizations
st.markdown("### Performance Overview")
col_left, col_right = st.columns(2)

with col_left:
    st.subheader("Revenue Trends")
    fig_rev = px.line(filtered_df, x="Date", y="Revenue", color="Region", 
                     template="plotly_dark", color_discrete_sequence=px.colors.qualitative.Pastel)
    st.plotly_chart(fig_rev, use_container_width=True)

with col_right:
    st.subheader("Sales by Region")
    fig_sales = px.pie(filtered_df, values="Sales", names="Region", 
                      template="plotly_dark", hole=0.4, color_discrete_sequence=px.colors.qualitative.Pastel)
    st.plotly_chart(fig_sales, use_container_width=True)

st.markdown("### Regional Distribution")
fig_bar = px.bar(filtered_df.groupby("Region")["Revenue"].sum().reset_index(), 
                 x="Region", y="Revenue", color="Region", template="plotly_dark")
st.plotly_chart(fig_bar, use_container_width=True)

# Footer
st.markdown("---")
st.markdown("Built with ❤️ by Syed Ubaid | [GitHub](https://github.com/syed-ubaid)")
