from distutils.ccompiler import gen_preprocess_options
import streamlit as st
from st_aggrid import AgGrid, GridOptionsBuilder, GridUpdateMode
import pandas as pd
import uuid

try:
  st.set_page_config(layout='wide')
except:
  pass

data = pd.DataFrame(
    [
        ["JW", "Project Leader"],
        ["SSS", "Administrador"],
        ["AJH", "Asset Manager"],
        ["BM", "Project Leader"],
        ["RHE", "Finance Officer"],
        ["AC", "Cleaner"],
        ["AMM", "Manager"],
        ["PS", "Manager"],
        ["KYL", "Manager"],
    ],
    columns=["User", "Position"],
)

@st.cache_data()
def getData():
    import pathlib
    path = pathlib.Path(__file__).parent / 'olympic-winners.json'
    data = pd.read_json(path)
    return data

data = getData()

# declaring gridOptions as a dictionary will be the preferred way now on.
gridOptions = {
  "columnDefs": [
    {
      "field": "athlete",
      "minWidth": 150,
      "headerCheckboxSelection": True,
      "checkboxSelection": True,
    },
    {
      "field": "age",
      "maxWidth": 90
    },
    {
      "field": "country",
      "minWidth": 150
    },
    {
      "field": "year",
      "maxWidth": 90
    },
    {
      "field": "date",
      "minWidth": 150
    },
    {
      "field": "sport",
      "minWidth": 150
    },
    {
      "field": "gold"
    },
    {
      "field": "silver"
    },
    {
      "field": "bronze"
    },
    {
      "field": "total"
    },
  ],
  "defaultColDef": {
    "flex": 1,
    "minWidth": 100,
    "filter": True,
    "enableRowGroup": True,
    "enablePivot": True,
    "enableValue": True,
  },
  "enableRangeSelection": True,
  "sideBar": True,
  "pagination": True,
  "rowSelection": "multiple",
  "suppressRowClickSelection": True,
  "suppressColumnMoveAnimation": True,
}

#uses a state variable as the grid key.
#to reset the grid, we change the key.
if not st.session_state.get('agGridKey',False):
    st.session_state['agGridKey']  = str(uuid.uuid4())

st.markdown("""
## Columns State  
You can work with the [grid state](https://www.ag-grid.com/javascript-data-grid/grid-state/) from you streamlit app.  
The example below reads the columns state by reading the `AgGridReturn.columns_state` and saving it to the session_state.   
The columns state is restored by including the `columns_state` object on the AgGrid call.
""")
st.divider()

cols =  st.columns(10)
with cols[0]:
    save_btn = st.button("Save columns state.")

with cols[1]:
    load_btn = st.button("Load columns state.")

with cols[2]: 
     reset_btn = st.button("Reset Grid")

gridHolder = st.columns(1)
st.divider()

cols =  st.columns(2)
with cols[0]:
    expander1 = st.expander("Current Columns State", expanded=True)

with cols[1]:
    expander2 =  st.expander("Saved Columns State", expanded=True)

if load_btn:
    columns_state = st.session_state.get("columns_state", None)
else:
    columns_state = None

if reset_btn:
     st.session_state['agGridKey']  = str(uuid.uuid4())

with gridHolder[0]:
    grid1 = AgGrid(
        data,
        gridOptions,
        height=400,
        update_on=["stateUpdated"],
        enable_enterprise_modules=True,
        key=st.session_state['agGridKey'],
        columns_state=columns_state,
    )

if save_btn:
    st.session_state['columns_state'] = grid1.columns_state

with expander1:
        st.write(grid1.columns_state)

with expander2:
        st.write(st.session_state.get("columns_state", None))

