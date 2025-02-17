import streamlit as st
import numpy as np
import pandas as pd
import plotly.express as px

# -------------------- Streamlit Page Configuration -------------------- #
st.set_page_config(page_title="Round-Up Savings Calculator", layout="wide")

# -------------------- Sidebar: User Inputs -------------------- #
st.sidebar.header("🔄 Customize Your Round-Up Savings")

# Round-up method selection
round_up_type = st.sidebar.selectbox(
    "Select Your Round-Up Type",
    ["Nearest $1", "Nearest $5", "Nearest $10"]
)

# User enters estimated monthly transactions
monthly_transactions = st.sidebar.number_input(
    "Avg. Transactions Per Month", min_value=1, value=50, step=1
)

# User enters estimated average transaction size
avg_transaction_size = st.sidebar.number_input(
    "Avg. Transaction Amount ($)", min_value=0.01, value=12.50, step=0.01
)

# User sets HYSA interest rate
hysa_apy = st.sidebar.number_input(
    "High-Yield Savings APY (%)", min_value=0.01, value=3.80, step=0.01
) / 100  # Convert to decimal

# User sets compounding frequency
compounding_periods = st.sidebar.selectbox(
    "Compounding Period",
    ["Daily", "Monthly", "Quarterly", "Annually"]
)

# Map compounding options to numeric values
compounding_map = {"Daily": 365, "Monthly": 12, "Quarterly": 4, "Annually": 1}
compounding_freq = compounding_map[compounding_periods]

# -------------------- Round-Up Savings Calculation -------------------- #
# Define round-up values based on selection
round_up_values = {"Nearest $1": 0.50, "Nearest $5": 2.50, "Nearest $10": 5.00}
round_up_amount = round_up_values[round_up_type]

# Estimate monthly round-up savings
monthly_savings = monthly_transactions * round_up_amount

# -------------------- 1-5 Year Savings Forecast with Compounding -------------------- #
years = np.arange(1, 6)  # Forecast for 1 to 5 years
savings_forecast = []

# Calculate compounded savings for each year using correct compounding formula
balance = 0
for year in years:
    for _ in range(compounding_freq * year):  # Apply compounding periods
        balance += monthly_savings
        balance *= (1 + hysa_apy / compounding_freq)
    savings_forecast.append(balance)

# Convert forecast to DataFrame
df_savings = pd.DataFrame({"Year": years, "Projected Savings ($)": savings_forecast})

# -------------------- Display Results -------------------- #
st.title("💰 Automated Round-Up Savings Calculator")

# Display estimated monthly savings
st.metric(label="💵 Estimated Monthly Savings", value=f"${monthly_savings:.2f}")

# Display interactive bar chart
st.write("### 📊 Projected Savings Over Time")
fig = px.bar(df_savings, x="Year", y="Projected Savings ($)", text="Projected Savings ($)",
             title=f"Projected Savings Growth ({round_up_type})",
             color_discrete_sequence=["purple"])

# Format chart
fig.update_traces(texttemplate="$%{text:,.2f}", textposition="outside")
fig.update_layout(yaxis_title="Total Savings ($)", xaxis_title="Years", 
                  yaxis_tickprefix="$", plot_bgcolor="white", 
                  yaxis=dict(showgrid=True, gridcolor="lightgray"))

st.plotly_chart(fig, use_container_width=True)

# -------------------- Summary Insights -------------------- #
st.write("### 📌 Key Takeaways")
st.info(f"📈 With a **{round_up_type}** strategy, you will save **${monthly_savings:.2f} per month**.")
st.info(f"💰 In **{years[-1]} years**, your savings will grow to **${savings_forecast[-1]:,.2f}** with a **{hysa_apy*100:.2f}% APY HYSA**.")
st.info(f"🔄 Changing the **round-up type or compounding period** will impact your total savings growth.")

# -------------------- Footer -------------------- #
st.markdown("---")
st.markdown("🔒 **DECC ensures secure, compliant multi-bank financial management for Americans abroad.**")
