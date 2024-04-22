
import streamlit as st
from st_aggrid import AgGrid
from st_aggrid.shared import getAllGridEvents
import pandas as pd

@st.cache_data
def get_data():
  return  pd.read_json("https://www.ag-grid.com/example-assets/olympic-winners.json")

df = get_data()

try:
  st.set_page_config(layout='wide')
except:
  pass


st.markdown("## Rerun Triggers")
st.markdown("""
AgGrid will trigger app rerun based on the event names supplied via `update_on` parameter.  
            
    update_on: list[string | tuple[sting, int]], optional
        Defines the events that will trigger a refresh and grid return on streamlit app.
        valid string named events are listed in https://www.ag-grid.com/javascript-data-grid/grid-events/.
        If a tuple[string, int] is present on the list, that event will be debounced by x milliseconds.
        for instance:
            if update_on = ['cellValueChanged', ("columnResized", 500)]
            Grid will return when cell values are changed AND when columns are resized, however the later will
            be debounced by 500 ms. More information about debounced functions 
            here: https://www.freecodecamp.org/news/javascript-debounce-example/
""")

gridEvents = sorted([i.get('name') for i in getAllGridEvents()])  

update_on = st.multiselect("Select events to trigger rerun", gridEvents, default=['cellValueChanged','selectionChanged', 'sortChanged', 'filterChanged'])




sample_data = df

tabs = st.tabs(["Grid", "Infered GridOptions", "Returned AgGrid Data", "Trigger Event Data"])

with tabs[0]:
    grid_return = AgGrid(df, update_on=update_on, update_mode='NO_UPDATE')

with tabs[1]:
    st.write(grid_return.grid_options)

with tabs[2]:
    st.write(grid_return.data)

with tabs[3]:
    st.write(grid_return.event_data)