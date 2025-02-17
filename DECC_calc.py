import streamlit as st
import numpy as np
import pandas as pd
import plotly.express as px

# -------------------- Streamlit Page Configuration -------------------- #
st.set_page_config(page_title="Round-Up Savings Calculator", layout="wide")

# -------------------- Sidebar: User Inputs -------------------- #
st.sidebar.header("🔄 Customize Your Round-Up Savings")

# Round-up type selection (Moved to sidebar navigation)
round_up_type = st.sidebar.radio(
    "Select Your Round-Up Type",
    ["Nearest $1", "Nearest $5", "Nearest $10"]
)

# User sets their monthly savings goal
monthly_savings_goal = st.sidebar.number_input(
    "🎯 Set Your Monthly Savings Goal ($)", min_value=10, value=500, step=10
)

# User enters estimated monthly transactions
monthly_transactions = st.sidebar.number_input(
    "📊 Avg. Transactions Per Month", min_value=1, value=50, step=1
)

# User sets HYSA interest rate
hysa_apy = st.sidebar.number_input(
    "🏦 High-Yield Savings APY (%)", min_value=0.01, value=3.80, step=0.01
) / 100  # Convert to decimal

# User sets compounding frequency
compounding_periods = st.sidebar.selectbox(
    "⏳ Compounding Period",
    ["Daily", "Monthly", "Quarterly", "Annually"]
)

# Map compounding options to numeric values
compounding_map = {"Daily": 365, "Monthly": 12, "Quarterly": 4, "Annually": 1}
compounding_freq = compounding_map[compounding_periods]

# -------------------- Round-Up Savings Calculation -------------------- #
# Define round-up values
round_up_values = {"Nearest $1": 0.50, "Nearest $5": 2.50, "Nearest $10": 5.00}

# Calculate estimated monthly savings for the selected round-up type
monthly_savings = monthly_transactions * round_up_values[round_up_type]

# -------------------- 1-5 Year Savings Forecast -------------------- #
years = np.arange(1, 6)  # Forecast for 1 to 5 years
savings_forecast = []

# Calculate compounded savings
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
st.metric(label=f"🔹 Estimated Monthly Savings ({round_up_type})", value=f"${monthly_savings:.2f}")

# Display interactive chart for the selected round-up type
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

# Display insights based on monthly goal progress
if monthly_savings >= monthly_savings_goal:
    st.success(f"🎯 You're on track! Your **estimated monthly savings** of **${monthly_savings:.2f}** meets or exceeds your goal of **${monthly_savings_goal:.2f}**.")
else:
    shortfall = monthly_savings_goal - monthly_savings
    st.warning(f"⚠️ You need to save **${shortfall:.2f}** more per month to meet your goal of **${monthly_savings_goal:.2f}**.")

# Long-term savings projection
st.info(f"💰 In **{years[-1]} years**, your savings will grow to **${savings_forecast[-1]:,.2f}** with a **{hysa_apy*100:.2f}% APY HYSA**.")

# -------------------- Footer -------------------- #
st.markdown("---")
st.markdown("🔒 **DECC ensures secure, compliant multi-bank financial management for Americans abroad.**")
