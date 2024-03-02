from distutils.ccompiler import gen_preprocess_options
import streamlit as st
from st_aggrid import AgGrid, GridOptionsBuilder, GridUpdateMode
import pandas as pd


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


columns_state = None

gb1 = GridOptionsBuilder.from_dataframe(data)
gb1.configure_selection(selection_mode="multiple", use_checkbox=True)
gb1.configure_side_bar()
go1 = gb1.build()


if st.button("Load Column State"):
    columns_state

    gridState = {
        "sideBar": {
            "visible": True,
            "position": "right",
            "openToolPanel": "filters",
            "toolPanels": {
                "filters": {"expandedGroupIds": [], "expandedColIds": ["Position"]},
                "columns": {"expandedGroupIds": []},
            },
        },
        "columnSizing": {
            "columnSizingModel": [
                {"colId": "User", "width": 200},
                {"colId": "Position", "width": 200},
            ]
        },
        "columnOrder": {"orderedColIds": ["User", "Position"]},
        "rowSelection": ["5"],
        "focusedCell": {"colId": "User", "rowIndex": 5, "rowPinned": None},
    }

    go1["initialState"] = gridState

grid1 = AgGrid(
    data,
    go1,
    update_mode=GridUpdateMode.MODEL_CHANGED | GridUpdateMode.COLUMN_RESIZED,
    enable_enterprise_modules=True,
)

st.write(grid1.grid_response)
