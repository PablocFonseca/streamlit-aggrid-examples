import streamlit as st
import pandas as pd
import json

from st_aggrid import AgGrid
from code_editor import code_editor


@st.cache_data
def get_data():
  return  pd.read_json("https://www.ag-grid.com/example-assets/olympic-winners.json")

df = get_data()

try:
  st.set_page_config(layout='wide')
except:
  pass

st.markdown("## Getting data from the Grid.")
st.markdown("""
Data from Grid can be retrived from `AgGridResponse.data`. Data will be sorted or filtered depending on `data_return_mode` parameter of aggrid call:  

>     data_return_mode : DataReturnMode, optional
>        Defines how the data will be retrieved from components client side. One of:
>            DataReturnMode.AS_INPUT             -> Returns grid data as inputed. Includes cell editions
>            DataReturnMode.FILTERED             -> Returns filtered grid data, maintains input order
>            DataReturnMode.FILTERED_AND_SORTED  -> Returns grid data filtered and sorted
>        Defaults to DataReturnMode.FILTERED_AND_SORTED.  
            
`AgGridResponse.data` will always return leaf nodes. To get data groups use `AgGridResponse.dataGroups`, which returns a dict of groupby columns as key and pandas DataFrames as values.
         

""")

groupby = st.checkbox("Group by country and age", False)

gridOptions = {
  'groupSelectsChildren':True,
  'columnDefs': [
    { 'field': "athlete", 'minWidth': 150 },
    { 'field': "country", 'minWidth': 150,'rowGroup':groupby, 'hide':groupby},
    { 'field': "age", 'maxWidth': 90,'rowGroup':groupby, 'hide':groupby},
    { 'field': "year", 'maxWidth': 90 },
    { 'field': "date", 'minWidth': 150 },
    { 'field': "sport", 'minWidth': 150 },
    { 'field': "gold" },
    { 'field': "silver" },
    { 'field': "bronze" },
    { 'field': "total" },
  ],
  'defaultColDef': {
    'flex': 1,
    'minWidth': 200,
  },
};


tabs = st.tabs(['Grid', 'AgGridReturn.data', 'AgGridReturn.groupedData'])

with tabs[0]:
  response = AgGrid(df, gridOptions, key='grid1')

with tabs[1]:
  st.write(response.data)

with tabs[2]:
  st.text("Showing first 10 groups: {")

  for i in response.dataGroups[0:10]:
    for k, v in i.items():
      cols = st.columns([4,10])
      with cols[0]:
        st.text(f"{tuple(k)}\t:")
      
      with cols[1]:
        st.dataframe(v)

  st.text("...")
  st.text("}")
