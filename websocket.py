import streamlit as st
from st_aggrid import AgGrid, JsCode
import time

JS_CODE_TEMPLATE = """
function onGridReady(params) {
    window.gridApi = params.api;
    const tickers = {tickers};
    tickers.forEach(ticker => {
        const socket = new WebSocket(`wss://stream.binance.com:9443/ws/${ticker}@trade`);
        socket.onmessage = function(event) {
            const trade = JSON.parse(event.data);
            const data = [{
                ticker: ticker.toUpperCase(),
                lastQuoteTimestamp: new Date(trade.T).toLocaleString(),
                lastQuote: trade.p
            }];
            const rowNode = window.gridApi.getRowNode(ticker.toUpperCase());
            if (!rowNode) {
                window.gridApi.applyTransaction({ add: data });
            } else {
                window.gridApi.applyTransaction({ update: data });
            }
        };
        socket.onerror = function(error) {
            console.error(`WebSocket error for ${ticker}:`, error);
        };
        socket.onclose = function() {
            console.warn(`WebSocket connection closed for ${ticker}.`);
        };
    });
}
"""


def main():
    st.title("Live Cryptocurrency Ticker Data")
    st.markdown("""
This app displays live cryptocurrency ticker data using Binance's WebSocket API.  
You can select tickers to subscribe to, and the grid updates in real-time with the latest trade data.  
Optionally, enable automatic app refresh with a configurable interval.
""")
    # fmt: off
    default_tickers = [
        "btcusdt", "ethusdt", "bnbusdt", "xrpusdt", "adausdt", "solusdt", "dogeusdt", 
        "dotusdt", "maticusdt", "shibusdt", "ltcusdt", "uniusdt", "linkusdt", "xlmusdt", 
        "trxusdt", "avaxusdt", "atomusdt", "vetusdt", "ftmusdt", "icpusdt", "egldusdt", 
        "axsbusdt", "manausdt", "sandusdt", "thetausdt", "hbarusdt", "algousdt", 
        "nearusdt", "xtzusdt", "chzusdt", "apeusdt", "qntusdt", "galausdt", "enjusdt", 
        "zecusdt", "dashusdt", "compusdt", "yfiusdt", "1inchusdt", "omgusdt", "wavesusdt", 
        "crvusdt", "snxusdt", "iotxusdt", "batusdt", "zilusdt", "hotusdt", "celousdt", 
        "arusdt", "lrcusdt", "kavausdt", "runeusdt", "sushiusdt", "ankrusdt", "storjusdt", 
        "ctsiusdt", "sklusdt", "oceanusdt", "roseusdt", "cvcusdt", "icxusdt", "ontusdt", 
        "iotusdt", "nknusdt", "scusdt", "dgbusdt", "hiveusdt", "xemusdt", "btsusdt", 
        "steemusdt", "stratusdt", "dashusdt", "zecusdt", "filusdt", "rvnusdt", "lunausdt", 
        "fttusdt", "chzusdt", "bchusdt", "etcusdt", "xmrusdt", "xlmusdt", "adausdt", 
        "vetusdt", "thetausdt", "enjusdt", "manausdt", "sandusdt", "axsbusdt", "egldusdt", 
        "hbarusdt", "algousdt", "nearusdt", "xtzusdt", "apeusdt", "qntusdt", "galausdt", 
        "roseusdt", "oceanusdt", "ctsiusdt", 
    ]
    # fmt: on

    default_selection = default_tickers[:25]
    selected_tickers = st.multiselect(
        "Select Tickers to Subscribe",
        options=default_tickers,
        default=default_selection,
    )

    js_code = JsCode(
        JS_CODE_TEMPLATE.replace("{tickers}", str(selected_tickers).lower())
    )

    enable_refresh = st.checkbox(
        "Enable automatic app refresh triggered by the grid", value=False
    )
    refresh_interval = 2000
    if enable_refresh:
        refresh_interval = st.slider(
            "Set refresh debounce interval (ms)",
            min_value=250,
            max_value=10000,
            value=2000,
            step=250,
        )

    if "previous_enable_refresh" not in st.session_state:
        st.session_state["previous_enable_refresh"] = enable_refresh
    if "previous_refresh_interval" not in st.session_state:
        st.session_state["previous_refresh_interval"] = refresh_interval

    if (enable_refresh != st.session_state["previous_enable_refresh"]) or (
        refresh_interval != st.session_state["previous_refresh_interval"]
    ):
        st.session_state["refresh_count"] = 0
        st.session_state["last_refresh_time"] = time.time()
        st.session_state["previous_enable_refresh"] = enable_refresh
        st.session_state["previous_refresh_interval"] = refresh_interval

    grid_options = {
        "columnDefs": [
            {"field": "ticker", "headerName": "Ticker"},
            {"field": "lastQuoteTimestamp", "headerName": "Last Quote Timestamp"},
            {
                "field": "lastQuote",
                "headerName": "Last Quote",
                "enableCellChangeFlash": True,
            },
        ],
        "defaultColDef": {"sortable": True, "filter": True, "resizable": True},
        "onGridReady": js_code,
        "getRowId": JsCode("function(params) { return params.data.ticker; }"),
    }

    update_on = [("rowDataUpdated", refresh_interval)] if enable_refresh else []

    r = AgGrid(
        None,
        gridOptions=grid_options,
        height=300,
        fit_columns_on_grid_load=True,
        allow_unsafe_jscode=True,
        update_on=update_on,
        key=f"WSGrid1_{refresh_interval}_{enable_refresh}",
    )

    with st.expander("Page Refresh Counter", expanded=True):
        if "refresh_count" not in st.session_state:
            st.session_state["refresh_count"] = 0
            st.session_state["last_refresh_time"] = time.time()

        if enable_refresh:
            st.session_state["refresh_count"] += 1

        current_time = time.time()
        interval = current_time - st.session_state["last_refresh_time"]
        st.session_state["last_refresh_time"] = current_time

        st.write(f"Page refresh count: {st.session_state['refresh_count']}")
        st.write(f"Time since last refresh: {interval:.2f} seconds")

    with st.expander("### Grid Return Data", expanded=True):
        st.json(r.data)


if __name__ == "__main__":
    main()
