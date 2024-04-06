import streamlit as st

try:
    st.set_page_config(layout="wide")
except:
    pass

st.markdown("# Getting Started with AgGrid")

st.markdown(
    """
## Instalation
Install streamlit-aggrid using pip or any package manager you prefer. Package is hosted on PyPi.
            
```
pip install streamlit-aggrid

```
"""
)


st.markdown(
    """
## Simple use
The simplest way to use the grid is to pass a pandas Dataframe to AgGrid call.   
Grid will infer column names and data types from the dataframe and render.  
The examplle below renders numbers right aligned and formats iso date columns.  

```python
from st_aggrid import AgGrid
import pandas as pd
  
df = pd.read_json("https://www.ag-grid.com/example-assets/olympic-winners.json")
grid_return = AgGrid(df)
```
"""
)


from st_aggrid import AgGrid
import pandas as pd


@st.cache_data
def get_data():
    return pd.read_json("https://www.ag-grid.com/example-assets/olympic-winners.json")


df = get_data()


tabs = st.tabs(["Grid", "Infered GridOptions", "Returned AgGrid Data"])

with tabs[0]:
    grid_return = AgGrid(df)

with tabs[1]:
    st.write(grid_return.grid_options)

with tabs[2]:
    st.write(grid_return.data)

st.markdown(
    """
## Grid Return
          
Grid return is an AgGridReturn object with props below:
"""
)
st.write(grid_return)
