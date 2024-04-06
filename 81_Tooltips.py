import streamlit as st
from st_aggrid import AgGrid, JsCode
import requests


@st.cache_data
def get_data():
  r = requests.get("https://www.ag-grid.com/example-assets/olympic-winners.json")
  return r.json()


columnDefs = [
  {
    'headerName': "Athlete",
    'field': "athlete",
    # here the Athlete column will tooltip the Country value
    'tooltipField': "country",
    'headerTooltip': "Tooltip for Athlete Column Header",
  },
  {
    'field': "age",
    'tooltipValueGetter': JsCode("""function(){return "Create any fixed message, e.g. This is the Athlete's Age"}"""),
    'headerTooltip': "Tooltip for Age Column Header",
  },
  {
    'field': "year",
    'tooltipValueGetter': JsCode("""function(p) {return "This is a dynamic tooltip using the value of " + p.value}"""),
    'headerTooltip': "Tooltip for Year Column Header",
  },
  {
    'headerName': "Hover For Tooltip",
    'headerTooltip': "Column Groups can have Tooltips also",
    'children': [
      {
        'field': "sport",
        'tooltipValueGetter': JsCode("""function(){return "Tooltip text about Sport should go here"}"""),
        'headerTooltip': "Tooltip for Sport Column Header",
      },
    ],
  },
];


gridOptions =  {
  'defaultColDef': {
    'flex': 1,
    'minWidth': 100,
  },
  'rowData': get_data(),
  'columnDefs': columnDefs,
  'tooltipShowDelay': 500,
};


st.markdown("""
This example implements the one described in [https://ag-grid.com/javascript-data-grid/tooltips/](https://ag-grid.com/javascript-data-grid/tooltips/)
""")

AgGrid(None, gridOptions, allow_unsafe_jscode=True)