import streamlit as st
import pandas as pd
import plotly.express as px


# ---------------- PAGE CONFIG ----------------

st.set_page_config(page_title="E-commerce Analytics Dashboard" layout="wide")


# ---------------- LOAD DATA ----------------

customer = pd.read_excel("Customersdata.xlsx")

orders = pd.read_excel("Ordersdata.xlsx")

product = pd.read_excel("Productsdata.xlsx")


# ---------------- DATA MODEL ----------------

df = orders.merge(customer,on="customer_id",how="left")

df = df.merge(product,on="product_id",how="left")


# ---------------- DATA CLEANING ----------------

df["order_date"] = pd.to_datetime(df["order_date"])


# Calculated Columns

df["Revenue"] = (df["quantity"] *df["selling_price"])

df["Profit"] = ((df["selling_price"] - df["cost_price"])* df["quantity"])


# ---------------- TITLE ----------------

st.title("🛒 E-commerce Data Analytics Dashboard")


# ---------------- SIDEBAR FILTERS ----------------

st.sidebar.header("Dashboard Filters")


city_filter = st.sidebar.multiselect("Select City",df["city"].unique(),default=df["city"].unique())


category_filter = st.sidebar.multiselect("Select Category",df["category"].unique(),default=df["category"].unique())


product_filter = st.sidebar.multiselect("Select Product",df["product_name"].unique(), default=df["product_name"].unique())


year_filter = st.sidebar.multiselect("Select Year",df["order_date"].dt.year.unique(),default=df["order_date"].dt.year.unique())



# Apply Filters

filtered_df = df[(df["city"].isin(city_filter)) & (df["category"].isin(category_filter)) & (df["product_name"].isin(product_filter)) & (df["order_date"].dt.year.isin(year_filter))]



# ---------------- KPI CARDS ----------------


revenue = filtered_df["Revenue"].sum()

orders_count = (filtered_df["order_id"].nunique())

customers = (filtered_df["customer_id"].nunique()
)

profit = filtered_df["Profit"].sum()

aov = revenue / orders_count if orders_count != 0 else 0



col1, col2, col3, col4, col5 = st.columns(5)


col1.metric( "Total Revenue",f"₹ {revenue:,.0f}")

col2.metric("Total Orders", orders_count)

col3.metric("Total Customers",customers)

col4.metric("Total Profit", f"₹ {profit:,.0f}")

col5.metric("Average Order Value",f"₹ {aov:,.0f}")



# ---------------- CHARTS ----------------


# 1 Monthly Revenue Trend

monthly = (filtered_df.groupby(filtered_df["order_date"].dt.to_period("M"))["Revenue"].sum().reset_index())

monthly["order_date"] = (monthly["order_date"].astype(str))


fig1 = px.line(monthly,x="order_date",y="Revenue",markers=True,title="Monthly Revenue Trend")

st.plotly_chart( fig1,use_container_width=True)



# 2 Revenue By Category

category_sales = (filtered_df.groupby("category")["Revenue"].sum().reset_index())


fig2 = px.bar(category_sales,x="category", y="Revenue",title="Revenue by Category")


st.plotly_chart(fig2,use_container_width=True)



# 3 Revenue By City

city_sales = (filtered_df.groupby("city") ["Revenue"].sum().reset_index())


fig3 = px.bar(city_sales, x="city",y="Revenue",title="Revenue by City")


st.plotly_chart(fig3,use_container_width=True)



# 4 Top Products

top_products = (filtered_df.groupby("product_name")["Revenue"].sum().sort_values(ascending=False).head(10).reset_index())


fig4 = px.bar(top_products,x="Revenue",y="product_name",orientation="h",title="Top 10 Products")


st.plotly_chart(fig4,use_container_width=True)



# 5 Customer Revenue

customer_sales = (filtered_df.groupby("customer_name")["Revenue"].sum().sort_values(ascending=False).head(10).reset_index())


fig5 = px.bar(customer_sales,x="Revenue",y="customer_name",orientation="h",title="Top Customers by Revenue")


st.plotly_chart(fig5,use_container_width=True)



# 6 Profit Analysis

profit_category = (filtered_df.groupby("category")["Profit"].sum().reset_index())


fig6 = px.pie(profit_category,names="category",values="Profit", title="Profit Contribution by Category")


st.plotly_chart(fig6,use_container_width=True)



# ---------------- DATA TABLE ----------------

st.subheader("Filtered Data")

st.dataframe( filtered_df, use_container_width=True)