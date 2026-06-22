import streamlit as st
st.title("Nassau Candy Dashboard")

st.metric("Total Orders", total_orders)
st.metric("Total Sales", round(total_sales))
st.metric("Total Profit", round(total_profit))
st.metric("Avg Lead Time", round(avg_lead_time, 2))