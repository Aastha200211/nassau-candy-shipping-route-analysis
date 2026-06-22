# 1. IMPORTS
import streamlit as st
import pandas as pd
import plotly.express as px

# 2. PAGE CONFIG
st.set_page_config(
    page_title="Nassau Candy Dashboard",
    page_icon="🍬",
    layout="wide"
)

# 3. CUSTOM CSS
st.markdown("""
<style>

/* Background */
.stApp {
    background-color: #f1f5f9;
}

.block-container{
    padding-top:2rem;
    padding-left:3rem;
    padding-right:3rem;
}

/* Dashboard Title */
h1 {
    color: #0f172a;
    text-align: center;
    font-weight: 800;
}

/* Subtitle */
h3 {
    color: #f97316;
    text-align: center;
}

/* KPI Cards */
[data-testid="stMetric"] {
    background-color: White;
    border: 2px solid #fed7aa;
    padding: 15px;
    border-radius: 15px;
    box-shadow: 0px 4px 12px rgba(0,0,0,0.08);
}

/* Sidebar */
[data-testid="stSidebar"] {
    background-color: #e2e8f0;
}

/* Tables */
[data-testid="stDataFrame"] {
    border-radius: 10px;
}

/* Buttons */
.stButton > button {
    background-color: #f97316;
    color: white;
    border-radius: 10px;
}

/* Success Box */
.stAlert {
    border-radius: 12px;
}

</style>
""", unsafe_allow_html=True)

# 4. LOAD DATA
df = pd.read_csv("Nassau Candy Distributor.csv")

# 5. DATE CONVERSION
df["Order Date"] = pd.to_datetime(df["Order Date"],format="%d-%m-%Y", errors="coerce")
df["Ship Date"] = pd.to_datetime(df["Ship Date"],format="%d-%m-%Y",errors="coerce")

# Remove invalid dates
df = df.dropna(subset=["Order Date", "Ship Date"])

# Lead Time
df["Lead Time"] = (df["Ship Date"] -df["Order Date"]).dt.days

# 7. SIDEBAR FILTERS
st.sidebar.header("Filters")
selected_region = st.sidebar.multiselect("Select Region",df["Region"].unique(),default=df["Region"].unique())
selected_shipmode = st.sidebar.multiselect( "Select Ship Mode",df["Ship Mode"].unique(),default=df["Ship Mode"].unique())

filtered_df = df[(df["Region"].isin(selected_region)) & (df["Ship Mode"].isin(selected_shipmode))]

#8. KPI CALCULATIONS
total_orders = filtered_df["Order ID"].nunique()
total_sales = filtered_df["Sales"].sum()
total_profit = filtered_df["Gross Profit"].sum()
avg_lead_time = filtered_df["Lead Time"].mean()

# 9. TITLE
st.title("🍬 Nassau Candy Shipping Analytics Dashboard")
st.markdown("### Factory-to-Customer Shipping Route Efficiency Analysis")

# 10. KPI CARDS
col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric("📦 Total Orders", total_orders)

with col2:
    st.metric("💰 Sales", f"${total_sales:,.0f}")

with col3:
    st.metric("📈 Profit", f"${total_profit:,.0f}")

with col4:
    st.metric("🚚 Avg Lead Time", f"{avg_lead_time:.2f} Days")

# 11. CHARTS
##sales
st.subheader("📊 Sales by Region")

region_sales = (filtered_df.groupby("Region")["Sales"].sum().reset_index())

fig = px.bar(region_sales,x="Region",y="Sales",title="Regional Sales Performance")

st.plotly_chart(fig, use_container_width=True)

#profit
st.subheader("💵 Profit Contribution")

region_profit = (filtered_df.groupby("Region")["Gross Profit"].sum().reset_index())

fig = px.pie(region_profit,names="Region",values="Gross Profit")

st.plotly_chart(fig, use_container_width=True)

#shipmode chart
st.subheader("🚚 Shipping Performance")

ship_mode = (filtered_df.groupby("Ship Mode")["Lead Time"].mean().reset_index())

fig = px.bar(ship_mode,x="Ship Mode",y="Lead Time",color="Ship Mode")

st.plotly_chart(fig, use_container_width=True)

# Product chart
st.subheader("🍭 Top Selling Products")

top_products = (filtered_df.groupby("Product Name")["Sales"].sum().sort_values(ascending=False).head(10).reset_index())

fig = px.bar(top_products,x="Sales",y="Product Name",orientation="h")

st.plotly_chart(fig, use_container_width=True)

st.subheader("🗺 Geographic Analysis")

col1, col2 = st.columns(2)

best_states = (filtered_df.groupby("State/Province")["Lead Time"].mean().sort_values().head(10))

worst_states = (filtered_df.groupby("State/Province")["Lead Time"].mean().sort_values(ascending=False).head(10))

with col1:
    st.write("### 🏆 Best Performing States")
    st.dataframe(best_states)

with col2:
    st.write("### ⚠ Worst Performing States")
    st.dataframe(worst_states)

# ROUTE EFFICIENCY ANALYSIS

st.subheader("🚚 Route Efficiency Analysis")

# Create Route Column
filtered_df["Route"] = (
    filtered_df["Region"].astype(str)
    + " → "
    + filtered_df["State/Province"].astype(str)
)

# Top Efficient Routes
top_routes = (
    filtered_df.groupby("Route")["Lead Time"]
    .mean()
    .sort_values()
    .head(10)
    .reset_index()
)

fig = px.bar(
    top_routes,
    x="Lead Time",
    y="Route",
    orientation="h",
    title="Top 10 Most Efficient Routes"
)

st.plotly_chart(fig, use_container_width=True)

# Top Delayed Routes
delayed_routes = (
    filtered_df.groupby("Route")["Lead Time"]
    .mean()
    .sort_values(ascending=False)
    .head(10)
    .reset_index()
)

fig = px.bar(
    delayed_routes,
    x="Lead Time",
    y="Route",
    orientation="h",
    title="Top 10 Delayed Routes"
)

st.plotly_chart(fig, use_container_width=True)

# 12. INSIGHTS
st.subheader("💡 Business Insights")

st.success("""
• Identify high-performing regions.

• Improve routes with high lead times.

• Encourage faster shipping modes.

• Focus on profitable products.

• Reduce bottlenecks in slow-performing states.
""")
