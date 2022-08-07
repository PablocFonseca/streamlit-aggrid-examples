import streamlit as st
import pandas as pd
import numpy as np
from st_aggrid import AgGrid, GridOptionsBuilder, JsCode, ColumnsAutoSizeMode

@st.cache()
def get_data():
    df = pd.DataFrame(
        np.random.randint(0, 100, 50).reshape(-1, 5), columns= list("abcde")
    )
    return df

df = get_data()
gb = GridOptionsBuilder.from_dataframe(df)
gb.configure_default_column(suppressMovable=True, filter=False, width=30)

columns_auto_size_mode = st.selectbox("Auto Size Mode:", list(ColumnsAutoSizeMode.__members__))
columns_auto_size_mode = ColumnsAutoSizeMode.__members__[columns_auto_size_mode]

AgGrid(df, gb.build(), allow_unsafe_jscode=True, fit_columns_on_grid_load=False, columns_auto_size_mode=columns_auto_size_mode)
