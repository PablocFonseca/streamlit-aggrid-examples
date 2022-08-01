from distutils.ccompiler import gen_preprocess_options
import streamlit as st
from st_aggrid import AgGrid, GridOptionsBuilder, GridUpdateMode
import pandas as pd


data = pd.DataFrame([
    ['JW', 'Project Leader'],
    ['SSS','Administrador'],
    ['AJH','Asset Manager'],
    ['BM','Project Leader'],
    ['RHE','Finance Officer'],
    ['AC','Cleaner'],
    ['AMM','Manager'],
    ['PS','Manager'],
    ['KYL','Manager']
    ], columns=['User','Position'])


columns_state = None

if st.button("Load Column State"):
    columns_state = [
        {
            "colId": "User",
            "width": 440,
            "hide": False,
            "pinned": None,
            "sort": None,
            "sortIndex": None,
            "aggFunc": None,
            "rowGroup": False,
            "rowGroupIndex": None,
            "pivot": False,
            "pivotIndex": None,
            "flex": None
        },
        {
            "colId": "Position",
            "width": 130,
            "hide": False,
            "pinned": None,
            "sort": "asc",
            "sortIndex": 0,
            "aggFunc": None,
            "rowGroup": False,
            "rowGroupIndex": None,
            "pivot": False,
            "pivotIndex": None,
            "flex": None
        }
]


gb1 = GridOptionsBuilder.from_dataframe(data)
gb1.configure_selection(selection_mode="multiple",use_checkbox=True)
go1 = gb1.build()

grid1 = AgGrid(
    data,
    go1,
    use_legacy_selected_rows=False, 
    key="fixed", 
    update_mode=GridUpdateMode.MODEL_CHANGED | GridUpdateMode.COLUMN_RESIZED,
    columns_state=columns_state
)

#st.write(((grid1.column_state)))
st.write(columns_state)
# gb2 = GridOptionsBuilder.from_dataframe(data)
# gb2.c