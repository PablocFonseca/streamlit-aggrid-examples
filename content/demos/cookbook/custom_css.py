import datetime

import numpy as np
import pandas as pd
import streamlit as st
from st_aggrid import AgGrid, GridOptionsBuilder


now = int(datetime.datetime.now().timestamp())
start_ts = now - 3 * 30 * 24 * 60 * 60


@st.cache_data
def make_data():
    df = pd.DataFrame(
        {
            "timestamp": np.random.randint(start_ts, now, 20),
            "side": [np.random.choice(["buy", "sell"]) for i in range(20)],
            "base": [np.random.choice(["JPY", "GBP", "CAD"]) for i in range(20)],
            "quote": [np.random.choice(["EUR", "USD"]) for i in range(20)],
            "amount": list(
                map(
                    lambda a: round(a, 2),
                    np.random.rand(20) * np.random.randint(1, 1000, 20),
                )
            ),
            "price": list(
                map(
                    lambda p: round(p, 5),
                    np.random.rand(20) * np.random.randint(1, 10, 20),
                )
            ),
        }
    )
    df["cost"] = round(df.amount * df.price, 2)
    df.insert(
        0,
        "datetime",
        df.timestamp.apply(lambda ts: datetime.datetime.fromtimestamp(ts)),
    )
    return df.sort_values("timestamp").drop("timestamp", axis=1)


df = make_data()
gb = GridOptionsBuilder.from_dataframe(df)

row_class_rules = {
    "trade-buy-green": "data.side == 'buy'",
    "trade-sell-red": "data.side == 'sell'",
}
gb.configure_grid_options(rowClassRules=row_class_rules)
grid_options = gb.build()

custom_css = {
    ".trade-buy-green": {"color": "green !important"},
    ".trade-sell-red": {"color": "red !important"},
}

st.title("rowClassRules Test")

st.markdown("""
This example demonstrates how to apply custom CSS classes to rows based on data values.
Rows are colored based on the 'side' column: green for 'buy' and red for 'sell'.
""")

AgGrid(df, theme="streamlit", custom_css=custom_css, gridOptions=grid_options)

with st.expander("Show code", expanded=False):
    st.code("""
import datetime
import numpy as np
import pandas as pd
import streamlit as st
from st_aggrid import AgGrid, GridOptionsBuilder

# Create sample trading data
now = int(datetime.datetime.now().timestamp())
start_ts = now - 3 * 30 * 24 * 60 * 60

df = pd.DataFrame({
    "timestamp": np.random.randint(start_ts, now, 20),
    "side": [np.random.choice(["buy", "sell"]) for i in range(20)],
    "base": [np.random.choice(["JPY", "GBP", "CAD"]) for i in range(20)],
    "quote": [np.random.choice(["EUR", "USD"]) for i in range(20)],
    "amount": [round(a, 2) for a in np.random.rand(20) * np.random.randint(1, 1000, 20)],
    "price": [round(p, 5) for p in np.random.rand(20) * np.random.randint(1, 10, 20)],
})

df["cost"] = round(df.amount * df.price, 2)
df.insert(0, "datetime", df.timestamp.apply(lambda ts: datetime.datetime.fromtimestamp(ts)))
df = df.sort_values("timestamp").drop("timestamp", axis=1)

# Define row class rules
row_class_rules = {
    "trade-buy-green": "data.side == 'buy'",
    "trade-sell-red": "data.side == 'sell'",
}

# Build grid options with row class rules
gb = GridOptionsBuilder.from_dataframe(df)
gb.configure_grid_options(rowClassRules=row_class_rules)
grid_options = gb.build()

# Define custom CSS for the classes
custom_css = {
    ".trade-buy-green": {"color": "green !important"},
    ".trade-sell-red": {"color": "red !important"},
}

# Display grid with custom CSS
AgGrid(df, theme="streamlit", custom_css=custom_css, gridOptions=grid_options)
""", language="python")
