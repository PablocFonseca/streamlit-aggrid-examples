import streamlit as st
import pandas as pd
import numpy as np

from st_aggrid import AgGrid, GridOptionsBuilder, JsCode

df = pd.DataFrame(
    "",
    index=range(10),
    columns=list("abcde"),
)

gb = GridOptionsBuilder.from_dataframe(df)
gb.configure_default_column(editable=True)

gb.configure_column(
    "a",
    cellEditor="agRichSelectCellEditor",
    cellEditorParams={"values": ["a", "b", "c"]},
    cellEditorPopup=True,
)

gb.configure_column(
    "b",
    cellEditor="agLargeTextCellEditor",
    cellEditorPopup=True,
    cellEditorParams={"maxLength": 100},
)

gb.configure_column(
    "c",
    cellEditor="agSelectCellEditor",
    cellEditorParams={
        "values": ["English", "Spanish", "French", "Portuguese", "(other)"],
    },
)

gb.configure_column(
    "d", cellEditor="agNumberCellEditor", cellEditorParams={"min": 0, "max": 100}
)


gb.configure_column(
    "e",
    cellEditor="agDateCellEditor",
    cellEditorParams={
        "min": "2000-01-01",
        "max": "2029-12-31",
    },
    valueFormatter=JsCode(
        "function(params) { console.log(params); return params.value }"
    ),
)

gb.configure_grid_options(enableRangeSelection=True)


gb.configure_grid_options(enableRangeSelection=True)

go = gb.build()
st.markdown("""
This example uses:   
`agRichSelectCellEditor` on column A.  
`agLargeTextCellEditor` on column B.  
`agSelectCellEditor` on column c with some language options.  
`agNumberCellEditor` on column d, limited to numbers between 0 and 100.  
`agDateStringCellEditor` on column
 e:
    
""")


tabs = st.tabs(["AgGrid", "gridOptions"])


with tabs[0]:
    response = AgGrid(
        df,
        gridOptions=go,
        enable_enterprise_modules=True,
        key="grid1",
        allow_unsafe_jscode=True,
    )

with tabs[1]:
    st.write(go)
