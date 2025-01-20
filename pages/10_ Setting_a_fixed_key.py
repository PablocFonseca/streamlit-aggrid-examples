import streamlit as st
from st_aggrid import AgGrid
import pandas as pd


@st.cache_data
def get_data():
    return pd.read_json("https://www.ag-grid.com/example-assets/olympic-winners.json")


df = get_data()

try:
    st.set_page_config(layout="wide")
except:
    pass

st.markdown("""
## Setting the __key__ parameter
Always set the key parameter for the grid, so it won't be destroyed between streamlit app refreshes. Also, 
If you need to render more than one Grid in your application, you have to set a different key parameter for each grid instance.  

On the exampe below left grid has no key set, while right grid has `key='right_grid'`. Data is sampled from the dataframe to simulate underlying data changes.  
            
```python
sample_data = df.sample(10)
left_grid = AgGrid(sample_data)
right_grid = AgGrid(sample_data, key='right_grid')
```
""")

st.button("Trigger Streamlit Refresh")
sample_data = df.sample(10)

left_col, right_col = st.columns(2)

with left_col:
    # for a strange reason dataframe is having dtypes changed. Investigate
    left_grid = AgGrid(sample_data)


with right_col:
    right_grid = AgGrid(sample_data, key="right_grid")
