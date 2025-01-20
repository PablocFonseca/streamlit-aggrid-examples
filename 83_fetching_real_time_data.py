import streamlit as st
from st_aggrid import AgGrid, JsCode, GridOptionsBuilder
import pandas as pd
import requests


def first_data():
    data = requests.get(
        "https://worldtimeapi.org/api/timezone/America/Sao_Paulo"
    ).json()
    return pd.Series(data).to_frame("Time").T


df = first_data()


# reference to onCellClicked handling functions here: https://ag-grid.com/javascript-data-grid/grid-events/#reference-selection-cellDoubleClicked
# This example function logs the params to the console and alerts which row/column was clicked.
fetchFunction = JsCode(r"""
    function (params){
        function update() {
            fetch('https://worldtimeapi.org/api/timezone/America/Sao_Paulo')
            .then(r=>r.json())
            //.then(console.log)
            .then(data=>params.api.applyTransaction({update:[data]}));
        //console.log(params.api.rowData);
        }
        setInterval(() => update(), 1000)                              
    }
""")

getRowId = JsCode(r"""
function(params) {
        return params.data.timezone;
    }

""")


gd = GridOptionsBuilder()

go = dict(onFirstDataRendered=fetchFunction, getRowId=getRowId)
go["columnDefs"] = [
    {"headerName": "timezone", "field": "timezone", "type": []},
    {"headerName": "unixtime", "field": "unixtime", "type": []},
    {"headerName": "datetime", "field": "datetime", "type": []},
    {"headerName": "client_ip", "field": "client_ip", "type": []},
]

tabs = st.tabs(["Grid", "Response"])


with tabs[0]:
    response = AgGrid(df, go, allow_unsafe_jscode=True)

with tabs[1]:
    st.write(response.data)

if "doubleClicked" in response.data.columns:
    lastDoubleClickedTs = pd.to_datetime(
        response.data["doubleClicked"], unit="ms"
    ).max()
    st.write(f"Last double click was {lastDoubleClickedTs} UTC")
