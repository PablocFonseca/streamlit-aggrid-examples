import streamlit as st
import pandas as pd
import numpy as np

from st_aggrid import AgGrid, GridOptionsBuilder, StAggridTheme, AgGridTheme

st.set_page_config(layout="wide")


@st.cache_data
def get_data():
    df = pd.DataFrame(
        np.random.randint(0, 100, 50).reshape(-1, 5),
        index=range(10),
        columns=list("abcde"),
    )
    return df


df = get_data()

st.markdown("""
Streamlit AgGrid implements most of AgGrid [theming API](https://www.ag-grid.com/javascript-data-grid/theming/). Custom Themes should be
specified using `StAggridTheme` class and passed to the grid _theme_ parameter or gridOptions theme key.  
If no custom theme is supplied, the grid will try to follow current streamlit theming for accent color, font, and light/dark modes. (Try playng with Edit active theme in settings menu.)
""")
st.write("")

cols = st.columns([2, 2])

with cols[0]:
    i, j = st.columns(2)
    with i:
        themeMode = st.radio(
            "Grid Theme :", ["Default (follows streamlit)", "Custom"], index=1
        )
    if themeMode == "Custom":
        with i:
            darkMode = st.toggle("Dark mode")
            borderEnabled = st.toggle("Border")
            backgroundColorPicker = st.color_picker("Background Color", value="#FFFFFF")
        with j:
            themeBase = st.selectbox("Theme Base:", ["quartz", "alpine", "balham"])
            fontSize = st.number_input(
                "Font size :", min_value=8, max_value=30, value=16
            )
            iconSet = st.selectbox(
                "Iconset :",
                ["iconSetAlpine", "iconSetQuartz", "iconSetMaterial"],
            )

        params = dict(
            fontSize=fontSize,
            rowBorder=borderEnabled,
            backgroundColor=backgroundColorPicker,
        )
        parts = [iconSet]
        if darkMode:
            parts.append("colorSchemeDark")

        theme = StAggridTheme(base=themeBase).withParams(**params).withParts(*parts)

        with cols[1]:
            st.markdown(f"""
                code used for custom theme:
                ```python
                custom_theme = (  
                    StAggridTheme(base="{themeBase}") 
                    .withParams({{
                        "fontSize": {params['fontSize']},
                        "rowBorder": {params['rowBorder']},
                        "backgroundColor": {params['backgroundColor']}
                    }})  
                    .withParts({parts})  
                )
                ```
            """)


gb = GridOptionsBuilder.from_dataframe(df)

response = AgGrid(
    df,
    editable=True,
    gridOptions=gb.build(),
    data_return_mode="filtered_and_sorted",
    update_mode="no_update",
    fit_columns_on_grid_load=True,
    theme=theme if themeMode == "Custom" else "streamlit",
    key="theming_grid",
)


st.stop()

available_themes = ["streamlit", "alpine", "balham", "material"]
selected_theme = st.selectbox("Theme", available_themes)

# if st.checkbox("Pre-select rows 4 and 6 when loading."):
#     gb.configure_selection("multiple", pre_selected_rows=["3", "5"])


selected_theme = (
    StAggridTheme(base="quartz")
    .withParams(fontSize=16)
    .withParts("iconSetAlpine", "colorSchemeDark")
)


response = AgGrid(
    df,
    editable=True,
    gridOptions=gb.build(),
    data_return_mode="filtered_and_sorted",
    update_mode="no_update",
    fit_columns_on_grid_load=True,
    theme=selected_theme,
    key="theming_grid",
)
