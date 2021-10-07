import yfinance as yf
import plotly.graph_objects as go

amzn = yf.Ticker("AMZN")

# get historical market data
hist = amzn.history(period="max")

# Reseting the index
hist = hist.reset_index()

# Converting the datatype to float
for i in ['Open', 'High', 'Close', 'Low']:
    hist[i] = hist[i].astype('float64')

# Creating Line chart using Plotly Graph_objects with Range slider and button
fig = go.Figure([go.Scatter(x=hist['Date'], y=hist['High'])])
fig.update_layout(
    title_text="Amazon Inc. Stock (Line chart)",
    yaxis_tickformat='M'
)
fig.update_xaxes(
    rangeslider_visible=True,
    rangeselector=dict(
        buttons=list([
            dict(count=1, label="1m", step="month",
                 stepmode="backward"),
            dict(count=6, label="6m", step="month",
                 stepmode="backward"),
            dict(count=1, label="YTD", step="year",
                 stepmode="todate"),
            dict(count=1, label="1y", step="year",
                 stepmode="backward"),
            dict(step="all")
        ])
    )
)
# Set x-axis title
fig.update_xaxes(title_text="Date")

# Set y-axes titles
fig.update_yaxes(title_text="Price")
fig.show()

###########################################################
# Creating candlestick chart with range slider
fig = go.Figure(data=[go.Candlestick(x=hist['Date'],
                                     open=hist['Open'],
                                     high=hist['High'],
                                     low=hist['Low'],
                                     close=hist['Close'], )])
fig.update_layout(
    title_text="Amazon Inc. Stock (Candlestick chart)",
    yaxis_tickformat='M'
)

fig.update_xaxes(
    rangeslider_visible=True,
    rangeselector=dict(
        buttons=list([
            dict(count=1, label="1m", step="month",
                 stepmode="backward"),
            dict(count=6, label="6m", step="month",
                 stepmode="backward"),
            dict(count=1, label="YTD", step="year",
                 stepmode="todate"),
            dict(count=1, label="1y", step="year",
                 stepmode="backward"),
            dict(step="all")
        ])
    )
)
# Set x-axes title
fig.update_xaxes(title_text="Date")

# Set y-axes title
fig.update_yaxes(title_text="Price")
fig.show()

###########################################################
# Creating OHLC Chart
fig = go.Figure(data=go.Ohlc(x=hist['Date'],
                             open=hist['Open'],
                             high=hist['High'],
                             low=hist['Low'],
                             close=hist['Close']))
fig.update_layout(
    title_text="Amazon Inc. Stock (OHLC chart)",
    yaxis_tickformat='M'
)
fig.update_xaxes(
    rangeslider_visible=True,
    rangeselector=dict(
        buttons=list([
            dict(count=1, label="1m", step="month",
                 stepmode="backward"),
            dict(count=6, label="6m", step="month",
                 stepmode="backward"),
            dict(count=1, label="YTD", step="year",
                 stepmode="todate"),
            dict(count=1, label="1y", step="year",
                 stepmode="backward"),
            dict(step="all")
        ])
    )
)
# Set x-axes title
fig.update_xaxes(title_text="Date")

# Set y-axes title
fig.update_yaxes(title_text="Price")
fig.show()

###########################################################
# Creating Volume Chart
fig = go.Figure(data=go.Bar(x=hist['Date'], y=hist['Volume'], name='Volume'))
fig.update_layout(
    title_text="Amazon Inc. Stock (Volume chart)",
    yaxis_tickformat='M'
)
fig.update_traces(marker_color='green')
fig.update_xaxes(
    rangeslider_visible=True,
    rangeselector=dict(
        buttons=list([
            dict(count=1, label="1m", step="month",
                 stepmode="backward"),
            dict(count=6, label="6m", step="month",
                 stepmode="backward"),
            dict(count=1, label="YTD", step="year",
                 stepmode="todate"),
            dict(count=1, label="1y", step="year",
                 stepmode="backward"),
            dict(step="all")
        ])
    )
)
# Set x-axes title
fig.update_xaxes(title_text="Date")

# Set y-axes title
fig.update_yaxes(title_text="Volume quantity")
fig.show()

###########################################################
# Creating Area Chart
import plotly.express as px

fig = px.area(x=hist["Date"], y=hist["High"], labels={'x': "Date", 'y': "Price"})
fig.update_layout(
    title_text="Amazon Inc. Stock (Area chart)",
    yaxis_tickformat='M'
)
fig.update_xaxes(
    rangeslider_visible=True,
    rangeselector=dict(
        buttons=list([
            dict(count=1, label="1m", step="month",
                 stepmode="backward"),
            dict(count=6, label="6m", step="month",
                 stepmode="backward"),
            dict(count=1, label="YTD", step="year",
                 stepmode="todate"),
            dict(count=1, label="1y", step="year",
                 stepmode="backward"),
            dict(step="all")
        ])
    )
)
# Set x-axes title
fig.update_xaxes(title_text="Date")

# Set y-axes title
fig.update_yaxes(title_text="Price")
fig.show()

####################################################
######### Plots ended. Describing data now #########
####################################################
# get stock info
print(amzn.info)

# show actions (dividends, splits)
print(amzn.actions)

# show dividends
print(amzn.dividends)

# show splits
print(amzn.splits)

# show financials
print(amzn.financials)
print(amzn.quarterly_financials)

# show major holders
print(amzn.major_holders)

# show institutional holders
print(amzn.institutional_holders)

# show balance sheet
print(amzn.balance_sheet)
print(amzn.quarterly_balance_sheet)

# show cashflow
print(amzn.cashflow)
print(amzn.quarterly_cashflow)

# show earnings
print(amzn.earnings)
print(amzn.quarterly_earnings)

# show sustainability
print(amzn.sustainability)

# show analysts recommendations
print(amzn.recommendations)

# show next event (earnings, etc)
print(amzn.calendar)

# show ISIN code - *experimental*
# ISIN = International Securities Identification Number
print(amzn.isin)
print("########################################################")
