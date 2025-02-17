import streamlit as st
import numpy as np
import pandas as pd
import plotly.express as px

# -------------------- Streamlit Page Configuration -------------------- #
st.set_page_config(page_title="Round-Up Savings Calculator", layout="wide")

# -------------------- Sidebar: User Inputs -------------------- #
st.sidebar.header("🔄 Customize Your Round-Up Savings")

# User sets their savings goal
savings_goal = st.sidebar.number_input(
    "🎯 Enter Your Savings Goal ($)", min_value=100, value=10000, step=100
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

# Estimate monthly savings for each round-up type
monthly_savings = {key: monthly_transactions * value for key, value in round_up_values.items()}

# -------------------- 1-5 Year Savings Forecast for All Round-Ups -------------------- #
years = np.arange(1, 6)  # Forecast for 1 to 5 years
savings_forecast = {key: [] for key in round_up_values.keys()}

# Calculate compounded savings for each round-up type
for key, monthly_contribution in monthly_savings.items():
    balance = 0
    for year in years:
        for _ in range(compounding_freq * year):  # Apply compounding periods
            balance += monthly_contribution
            balance *= (1 + hysa_apy / compounding_freq)
        savings_forecast[key].append(balance)

# Convert forecast to DataFrame for visualization
df_savings = pd.DataFrame({
    "Year": np.tile(years, 3),
    "Projected Savings ($)": np.concatenate([savings_forecast["Nearest $1"], 
                                             savings_forecast["Nearest $5"], 
                                             savings_forecast["Nearest $10"]]),
    "Round-Up Type": np.repeat(["Nearest $1", "Nearest $5", "Nearest $10"], len(years))
})

# -------------------- Display Results -------------------- #
st.title("💰 Automated Round-Up Savings Calculator")

# Display estimated monthly savings for all types
st.write("### 📊 Monthly Round-Up Savings")
st.metric(label="🔹 Nearest $1 Round-Up", value=f"${monthly_savings['Nearest $1']:.2f}")
st.metric(label="🔹 Nearest $5 Round-Up", value=f"${monthly_savings['Nearest $5']:.2f}")
st.metric(label="🔹 Nearest $10 Round-Up", value=f"${monthly_savings['Nearest $10']:.2f}")

# Display interactive comparison chart
st.write("### 📊 Projected Savings Over Time (Comparison)")
fig = px.bar(df_savings, x="Year", y="Projected Savings ($)", color="Round-Up Type",
             title="Comparison of Round-Up Savings ($1 vs $5 vs $10)",
             barmode="group", color_discrete_map={
                 "Nearest $1": "blue",
                 "Nearest $5": "purple",
                 "Nearest $10": "green"
             })

# Format chart
fig.update_layout(yaxis_title="Total Savings ($)", xaxis_title="Years", 
                  yaxis_tickprefix="$", plot_bgcolor="white", 
                  yaxis=dict(showgrid=True, gridcolor="lightgray"))

st.plotly_chart(fig, use_container_width=True)

# -------------------- Summary Insights -------------------- #
st.write("### 📌 Key Takeaways")
st.info(f"💰 With a **Nearest $5 Round-Up**, your savings in **{years[-1]} years** will be **${savings_forecast['Nearest $5'][-1]:,.2f}**.")
st.info(f"🎯 Your goal is **${savings_goal:,.2f}**, and you're projected to reach **{(savings_forecast['Nearest $5'][-1] / savings_goal) * 100:.1f}%** of it.")
st.info(f"💡 Want to reach your goal **faster**? Try switching to a **Nearest $10 Round-Up** or increasing transaction volume.")

# -------------------- Footer -------------------- #
st.markdown("---")
st.markdown("🔒 **DECC ensures secure, compliant multi-bank financial management for Americans abroad.**")
