import yfinance as yf
import streamlit as st
import pandas as pd
import plotly.express as px
from datetime import datetime, timedelta

st.set_page_config(page_title="Stock Analysis App", layout="wide")

# Load company names and tickers from CSV
@st.cache_data
def load_data():
    data = pd.read_csv("stocks_us.csv")
    return data

data = load_data()

# Sidebar for user input
st.sidebar.header("Select Company")
selected_company = st.sidebar.selectbox("Select a company", data["Name"])
ticker = data[data["Name"] == selected_company]["Ticker"].values[0]

# User-friendly date range selection
st.sidebar.header("Date Range")
end_date = st.sidebar.date_input("End Date", datetime.today())
start_date = st.sidebar.date_input("Start Date", end_date - timedelta(days=365))

# Fetch stock data using yfinance
stock_data = yf.download(ticker, start=start_date, end=end_date)

# Interactive Price Chart
st.header(f"Price Chart for {selected_company} ({ticker})")
fig = px.line(stock_data, x=stock_data.index, y="Close", title="Stock Price")
st.plotly_chart(fig, use_container_width=True)

# Volume Analysis
st.header("Volume Analysis")
volume_fig = px.bar(stock_data, x=stock_data.index, y="Volume", title="Trading Volume")
st.plotly_chart(volume_fig, use_container_width=True)

# Comparative Analysis
st.header("Comparative Analysis")
selected_companies = st.multiselect("Select companies to compare", data["Name"])
selected_tickers = data[data["Name"].isin(selected_companies)]["Ticker"].tolist()
comparison_data = yf.download(selected_tickers, start=start_date, end=end_date)["Close"]
comparison_fig = px.line(comparison_data, title="Comparative Stock Prices")
st.plotly_chart(comparison_fig, use_container_width=True)

# Fundamental Analysis
st.header("Fundamental Analysis")
info = yf.Ticker(ticker).info
st.write(f"**Sector:** {info['sector']}")
st.write(f"**Industry:** {info['industry']}")
st.write(f"**Market Cap:** {info['marketCap']}")
st.write(f"**Gross Profits:** {info['grossProfits']}")


# News Overlay
st.header("News Overlay")
news = yf.Ticker(ticker).news
for item in news:
    st.write(f"- [{item['title']}]({item['link']})")

st.sidebar.text("This is a basic example. Enhance and customize it further based on your needs.")
