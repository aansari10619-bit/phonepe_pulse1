import streamlit as st
import pandas as pd
import plotly.express as px
from sqlalchemy import create_engine

# -------------------------------
# 1️⃣ App Title and Setup
# -------------------------------
st.set_page_config(page_title="PhonePe Data Insights", layout="wide")
st.title("📊 PhonePe Data Visualization Dashboard")

# -------------------------------
# 2️⃣ PostgreSQL Connection
# -------------------------------
# Database credentials
db_user = 'ansari'
db_password = '1234'
db_host = 'localhost'
db_port = '5433'
db_name = 'phonepe_pulse'

# Create SQLAlchemy engine
engine = create_engine(f'postgresql+psycopg2://{db_user}:{db_password}@{db_host}:{db_port}/{db_name}')


# -------------------------------
# 3️⃣ Load Data from PostgreSQL
# -------------------------------
@st.cache_data
def load_data_from_postgres():
    data = {
        "aggregated_insurance": pd.read_sql("SELECT * FROM aggregated_insurance", engine),
        "aggregated_transaction": pd.read_sql("SELECT * FROM aggregated_transaction", engine),
        "aggregated_user": pd.read_sql("SELECT * FROM aggregated_user", engine),
        "map_insurance": pd.read_sql("SELECT * FROM map_insurance", engine),
        "map_transaction": pd.read_sql("SELECT * FROM map_transaction", engine),
        "top_insurance_dist": pd.read_sql("SELECT * FROM top_insurance_dist", engine),
        "top_transaction_dist": pd.read_sql("SELECT * FROM top_transaction_dist", engine),
    }
    return data

data = load_data_from_postgres()

# -------------------------------
# 4️⃣ Scenario Dropdown
# -------------------------------
scenarios = [
    "Decoding Transaction Dynamics on PhonePe",
    "Device Dominance and User Engagement Analysis",
    "Insurance Penetration and Growth Potential Analysis",
    "Transaction Analysis for Market Expansion",
    "User Engagement and Growth Strategy"  # 🆕 Added third scenario
]

scenario = st.selectbox("Select Scenario:", scenarios)


# -------------------------------
# 5️⃣ Scenario 1: Transaction Dynamics
# -------------------------------
if scenario == "Decoding Transaction Dynamics on PhonePe":
    st.markdown("""
    ### 📘 Scenario 1: Decoding Transaction Dynamics on PhonePe
    PhonePe identified variations in transaction behavior across states, quarters, and payment categories.  
    The goal is to analyze these variations and uncover actionable insights.
    """)

    questions = {
        "Q1: Which states have the highest transaction amounts over years?": "aggregated_transaction",
        "Q2: How does transaction type vary across states?": "aggregated_transaction",
        "Q3: How have user registrations and app opens changed over time?": "aggregated_user",
        "Q4: What is the distribution of insurance transactions by state?": "aggregated_insurance",
        "Q5: Which districts contribute most to total transaction volume?": "map_transaction"
    }

    question = st.selectbox("Select Business Question:", list(questions.keys()))

    if question == "Q1: Which states have the highest transaction amounts over years?":
        df = data["aggregated_transaction"]
        df_grouped = df.groupby(["Year", "State"])["Transaction_Amount"].sum().reset_index()
        fig = px.bar(df_grouped, x="State", y="Transaction_Amount", color="Year",
                     title="Transaction Amount by State and Year", barmode="group")
        st.plotly_chart(fig, use_container_width=True)

    elif question == "Q2: How does transaction type vary across states?":
        df = data["aggregated_transaction"]
        fig = px.sunburst(df, path=["State", "Transaction_Type"], values="Transaction_Amount",
                          title="Transaction Type Distribution by State")
        st.plotly_chart(fig, use_container_width=True)

    elif question == "Q3: How have user registrations and app opens changed over time?":
        df = data["aggregated_user"]
        df_sum = df.groupby(["Year", "Quarter"]).sum().reset_index()
        fig = px.line(df_sum, x="Year", y=["Registered_Users", "App_Opens"], markers=True,
                      title="User Growth and App Opens Over Time")
        st.plotly_chart(fig, use_container_width=True)

    elif question == "Q4: What is the distribution of insurance transactions by state?":
        df = data["aggregated_insurance"]
        df_state = df.groupby("State")["Transaction_Amount"].sum().reset_index()
        fig = px.pie(df_state, names="State", values="Transaction_Amount",
                     title="Insurance Transaction Amount by State")
        st.plotly_chart(fig, use_container_width=True)

    elif question == "Q5: Which districts contribute most to total transaction volume?":
        df = data["map_transaction"]
        df_top = df.groupby("District")["Transaction_Amount"].sum().reset_index().sort_values(
            by="Transaction_Amount", ascending=False).head(10)
        fig = px.bar(df_top, x="District", y="Transaction_Amount", color="Transaction_Amount",
                     title="Top 10 Districts by Transaction Amount")
        st.plotly_chart(fig, use_container_width=True)

# -------------------------------
# 6️⃣ Scenario 2: Device Dominance & User Engagement
# -------------------------------
elif scenario == "Device Dominance and User Engagement Analysis":
    st.markdown("""
    ### 📱 Scenario 2: Device Dominance and User Engagement Analysis
    PhonePe aims to understand how user engagement varies across different device brands and regions.
    The objective is to analyze how registered users and app opens differ by device usage trends.
    """)

    questions = {
        "Q1: How do registered users vary across states and years?": "aggregated_user",
        "Q2: Which states show the highest app engagement (App Opens)?": "aggregated_user",
        "Q3: What is the relationship between registered users and app opens?": "aggregated_user",
        "Q4: How does user engagement vary quarterly across years?": "aggregated_user",
        "Q5: What are the top underperforming regions in terms of app opens vs registered users?": "aggregated_user"
    }

    question = st.selectbox("Select Business Question:", list(questions.keys()))

    if question == "Q1: How do registered users vary across states and years?":
        df = data["aggregated_user"]
        df_grouped = df.groupby(["State", "Year"])["Registered_Users"].sum().reset_index()
        fig = px.bar(df_grouped, x="State", y="Registered_Users", color="Year",
                     title="Registered Users by State and Year", barmode="group")
        st.plotly_chart(fig, use_container_width=True)

    elif question == "Q2: Which states show the highest app engagement (App Opens)?":
        df = data["aggregated_user"]
        df_state = df.groupby("State")["App_Opens"].sum().reset_index().sort_values(by="App_Opens", ascending=False)
        fig = px.bar(df_state.head(10), x="State", y="App_Opens", color="App_Opens",
                     title="Top 10 States by App Engagement (App Opens)")
        st.plotly_chart(fig, use_container_width=True)

    elif question == "Q3: What is the relationship between registered users and app opens?":
        df = data["aggregated_user"]
        fig = px.scatter(df, x="Registered_Users", y="App_Opens", color="Year",
                         title="Correlation between Registered Users and App Opens",
                         hover_data=["State", "Quarter"])
        st.plotly_chart(fig, use_container_width=True)

    elif question == "Q4: How does user engagement vary quarterly across years?":
        df = data["aggregated_user"]
        df_quarter = df.groupby(["Year", "Quarter"])["App_Opens"].sum().reset_index()
        fig = px.line(df_quarter, x="Quarter", y="App_Opens", color="Year",
                      markers=True, title="Quarterly App Engagement Over Years")
        st.plotly_chart(fig, use_container_width=True)

    elif question == "Q5: What are the top underperforming regions in terms of app opens vs registered users?":
        df = data["aggregated_user"]
        df["Engagement_Ratio"] = df["App_Opens"] / (df["Registered_Users"] + 1)
        df_sorted = df.groupby("State")["Engagement_Ratio"].mean().reset_index().sort_values(by="Engagement_Ratio")
        fig = px.bar(df_sorted.head(10), x="State", y="Engagement_Ratio", color="Engagement_Ratio",
                     title="Top 10 Underperforming States (App Opens / Registered Users)")
        st.plotly_chart(fig, use_container_width=True)

# -------------------------------
# 7️⃣ Scenario 3: Insurance Penetration and Growth Potential Analysis
# -------------------------------
elif scenario == "Insurance Penetration and Growth Potential Analysis":
    st.markdown("""
    ### 🧾 Scenario 3: Insurance Penetration and Growth Potential Analysis
    PhonePe has ventured into the insurance domain, providing users with policy options.  
    This analysis explores the growth trajectory of insurance transactions and identifies  
    untapped opportunities for expansion across states.
    """)

    questions = {
        "Q1: Which states show the highest total insurance transaction amounts?": "aggregated_insurance",
        "Q2: How has insurance transaction volume grown over time across states?": "aggregated_insurance",
        "Q3: Which districts are driving the majority of insurance transactions?": "map_insurance",
        "Q4: What are the top-performing districts by insurance transaction amount?": "top_insurance_dist",
        "Q5: Which states have the highest average transaction amount per insurance policy?": "aggregated_insurance"
    }

    question = st.selectbox("Select Business Question:", list(questions.keys()))

    # Q1: Highest total insurance transaction amounts
    if question == "Q1: Which states show the highest total insurance transaction amounts?":
        df = data["aggregated_insurance"]
        df_state = df.groupby("State")["Transaction_Amount"].sum().reset_index().sort_values(by="Transaction_Amount", ascending=False)
        fig = px.bar(df_state, x="State", y="Transaction_Amount", color="Transaction_Amount",
                     title="Total Insurance Transaction Amount by State")
        st.plotly_chart(fig, use_container_width=True)

    # Q2: Growth over time across states
    elif question == "Q2: How has insurance transaction volume grown over time across states?":
        df = data["aggregated_insurance"]
        df_grouped = df.groupby(["Year", "State"])["Transaction_Count"].sum().reset_index()
        fig = px.line(df_grouped, x="Year", y="Transaction_Count", color="State",
                      markers=True, title="Insurance Transaction Volume Growth by State")
        st.plotly_chart(fig, use_container_width=True)

    # Q3: Districts driving majority of insurance transactions
    elif question == "Q3: Which districts are driving the majority of insurance transactions?":
        df = data["map_insurance"]
        df_top = df.groupby("District")["Transaction_Amount"].sum().reset_index().sort_values(by="Transaction_Amount", ascending=False).head(10)
        fig = px.bar(df_top, x="District", y="Transaction_Amount", color="Transaction_Amount",
                     title="Top 10 Districts Driving Insurance Transactions")
        st.plotly_chart(fig, use_container_width=True)

    # Q4: Top-performing districts by transaction amount
    elif question == "Q4: What are the top-performing districts by insurance transaction amount?":
        df = data["top_insurance_dist"]
        df_top = df.groupby("District")["Transaction_Amount"].sum().reset_index().sort_values(by="Transaction_Amount", ascending=False)
        fig = px.bar(df_top, x="District", y="Transaction_Amount", color="Transaction_Amount",
                     title="Top Performing Districts in Insurance Transactions")
        st.plotly_chart(fig, use_container_width=True)

    # Q5: States with highest average transaction amount per policy
    elif question == "Q5: Which states have the highest average transaction amount per insurance policy?":
        df = data["aggregated_insurance"]
        df["Avg_Transaction_Value"] = df["Transaction_Amount"] / (df["Transaction_Count"] + 1)
        df_avg = df.groupby("State")["Avg_Transaction_Value"].mean().reset_index().sort_values(by="Avg_Transaction_Value", ascending=False)
        fig = px.bar(df_avg, x="State", y="Avg_Transaction_Value", color="Avg_Transaction_Value",
                     title="Average Insurance Transaction Value per State")
        st.plotly_chart(fig, use_container_width=True)


# -------------------------------
# 8️⃣ Scenario 4: Transaction Analysis for Market Expansion
# -------------------------------
elif scenario == "Transaction Analysis for Market Expansion":
    st.markdown("""
    ### 🌍 Scenario 4: Transaction Analysis for Market Expansion
    PhonePe aims to understand transaction behavior across states and districts to identify 
    potential markets for expansion. This analysis highlights regions with high activity 
    and areas showing untapped growth opportunities.
    """)

    questions = {
        "Q1: Which states record the highest total transaction amounts across years?": "aggregated_transaction",
        "Q2: How has total transaction volume changed over time?": "aggregated_transaction",
        "Q3: Which transaction types dominate across different states?": "aggregated_transaction",
        "Q4: Which districts contribute most to total transaction volume?": "map_transaction",
        "Q5: What are the top 10 districts showing potential for market expansion?": "top_transaction_dist"
    }

    question = st.selectbox("Select Business Question:", list(questions.keys()))

    # Q1: States with highest transaction amounts
    if question == "Q1: Which states record the highest total transaction amounts across years?":
        df = data["aggregated_transaction"]
        df_state = df.groupby("State")["Transaction_Amount"].sum().reset_index().sort_values(by="Transaction_Amount", ascending=False)
        fig = px.bar(df_state, x="State", y="Transaction_Amount", color="Transaction_Amount",
                     title="Total Transaction Amount by State")
        st.plotly_chart(fig, use_container_width=True)

    # Q2: Transaction volume growth over time
    elif question == "Q2: How has total transaction volume changed over time?":
        df = data["aggregated_transaction"]
        df_year = df.groupby("Year")["Transaction_Count"].sum().reset_index()
        fig = px.line(df_year, x="Year", y="Transaction_Count", markers=True,
                      title="Transaction Volume Growth Over Years")
        st.plotly_chart(fig, use_container_width=True)

    # Q3: Dominant transaction types by state
    elif question == "Q3: Which transaction types dominate across different states?":
        df = data["aggregated_transaction"]
        fig = px.sunburst(df, path=["State", "Transaction_Type"], values="Transaction_Amount",
                          title="Dominant Transaction Types Across States")
        st.plotly_chart(fig, use_container_width=True)

    # Q4: Top contributing districts
    elif question == "Q4: Which districts contribute most to total transaction volume?":
        df = data["map_transaction"]
        df_top = df.groupby("District")["Transaction_Amount"].sum().reset_index().sort_values(by="Transaction_Amount", ascending=False).head(10)
        fig = px.bar(df_top, x="District", y="Transaction_Amount", color="Transaction_Amount",
                     title="Top 10 Districts by Transaction Volume")
        st.plotly_chart(fig, use_container_width=True)

    # Q5: Districts with potential for market expansion
    elif question == "Q5: What are the top 10 districts showing potential for market expansion?":
        df = data["top_transaction_dist"]
        df_sorted = df.groupby("District")["Transaction_Amount"].sum().reset_index().sort_values(by="Transaction_Amount", ascending=True).head(10)
        fig = px.bar(df_sorted, x="District", y="Transaction_Amount", color="Transaction_Amount",
                     title="Top 10 Emerging Districts for Market Expansion")
        st.plotly_chart(fig, use_container_width=True)


# -------------------------------
# 9️⃣ Scenario 5: User Engagement and Growth Strategy
# -------------------------------
elif scenario == "User Engagement and Growth Strategy":
    st.markdown("""
    ### 👥 Scenario 5: User Engagement and Growth Strategy
    PhonePe aims to enhance its market position by analyzing user engagement metrics across states.
    This analysis explores trends in registered users and app opens to uncover key growth opportunities.
    """)

    questions = {
        "Q1: Which states have the highest number of registered users over time?": "aggregated_user",
        "Q2: How has app engagement evolved across years and quarters?": "aggregated_user",
        "Q3: What is the relationship between registered users and app opens across states?": "aggregated_user",
        "Q4: Which states show the strongest growth in user registration?": "aggregated_user",
        "Q5: Which states have the highest app engagement ratio (App Opens per Registered User)?": "aggregated_user"
    }

    question = st.selectbox("Select Business Question:", list(questions.keys()))

    # Q1: States with highest registered users
    if question == "Q1: Which states have the highest number of registered users over time?":
        df = data["aggregated_user"]
        df_grouped = df.groupby(["State", "Year"])["Registered_Users"].sum().reset_index()
        fig = px.bar(df_grouped, x="State", y="Registered_Users", color="Year",
                     title="Registered Users by State and Year", barmode="group")
        st.plotly_chart(fig, use_container_width=True)

    # Q2: App engagement trends
    elif question == "Q2: How has app engagement evolved across years and quarters?":
        df = data["aggregated_user"]
        df_time = df.groupby(["Year", "Quarter"])["App_Opens"].sum().reset_index()
        fig = px.line(df_time, x="Quarter", y="App_Opens", color="Year",
                      markers=True, title="App Engagement Over Time (Yearly & Quarterly)")
        st.plotly_chart(fig, use_container_width=True)

    # Q3: Relationship between registered users and app opens
    elif question == "Q3: What is the relationship between registered users and app opens across states?":
        df = data["aggregated_user"]
        fig = px.scatter(df, x="Registered_Users", y="App_Opens", color="Year",
                         title="Correlation Between Registered Users and App Opens",
                         hover_data=["State", "Quarter"])
        st.plotly_chart(fig, use_container_width=True)

    # Q4: Strongest growth in user registration
    elif question == "Q4: Which states show the strongest growth in user registration?":
        df = data["aggregated_user"]
        df_growth = df.groupby(["State", "Year"])["Registered_Users"].sum().reset_index()
        df_growth = df_growth.sort_values(by=["Year", "Registered_Users"], ascending=[True, False])
        fig = px.line(df_growth, x="Year", y="Registered_Users", color="State",
                      markers=True, title="Yearly Growth in Registered Users by State")
        st.plotly_chart(fig, use_container_width=True)

    # Q5: Highest engagement ratio (App Opens / Registered Users)
    elif question == "Q5: Which states have the highest app engagement ratio (App Opens per Registered User)?":
        df = data["aggregated_user"]
        df["Engagement_Ratio"] = df["App_Opens"] / (df["Registered_Users"] + 1)
        df_ratio = df.groupby("State")["Engagement_Ratio"].mean().reset_index().sort_values(by="Engagement_Ratio", ascending=False)
        fig = px.bar(df_ratio, x="State", y="Engagement_Ratio", color="Engagement_Ratio",
                     title="App Engagement Ratio by State (App Opens per Registered User)")
        st.plotly_chart(fig, use_container_width=True)


# -------------------------------
# 7️⃣ Footer
# -------------------------------
st.markdown("""
---
✅ Built with **Streamlit + Plotly + Pandas**  
🗄️ Data Source: PostgreSQL database — `phonepe_pulse`
""")
