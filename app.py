import streamlit as st
from components.ui_components import inject_banner_styles, render_banner, render_premium_button

pages = {
    "": [
        st.Page("content/landing.py", title="Streamlit-Aggrid", icon="🏠"),
        st.Page("content/getting_started.py", title="Getting Started", icon="🚀"),
    ],
    "📍 User Guide": [
        st.Page("content/docs/10_configuration.py", title="Basic Configuration", icon="⚙️"),
        st.Page("content/docs/20_column_configuration.py", title="Column Configuration", icon="📊"),  
        st.Page("content/docs/30_grid_options_builder.py", title="GridOptions Builder", icon="🔧"),
        st.Page("content/docs/40_data_editing.py", title="Data Editing", icon="✏️"),  
        st.Page("content/docs/50_row_selection.py", title="Row Selection", icon="✅"),   
        st.Page("content/docs/60_aggrid_parameters.py", title="AgGrid Function Parameters", icon="📋"), 
        st.Page("content/docs/70_grid_events.py", title="Grid Events & Callbacks", icon="🔔"),
        st.Page("content/docs/80_server_synch.py", title="Server Synch Strategy", icon="🔄"),
        st.Page("content/docs/90_returned_data.py", title="Working with Returned Data", icon="📤"),
        st.Page("content/docs/100_JsCode.py", title="Custom JavaScript Code", icon="🧑‍💻"),
        st.Page("content/docs/110_Themes.py", title="Themes & Visual Customization", icon="🎨"),
        st.Page("content/docs/120_performance.py", title="Performance & Large Datasets", icon="⚡"),  
        st.Page("content/docs/130_Licencing.py", title="Enterprise Features & Licensing", icon="💼"), 
    ],
    "💻 Demos": [
        st.Page("content/demos/cookbook/90_main_example.py", title="Main Example"),
        st.Page("content/demos/cookbook/12_Data_Input.py", title="Data Input"),
        st.Page("content/demos/cookbook/20_cell_renderer_class_example.py", title="Cell Renderer Class"),
        st.Page("content/demos/cookbook/30_virtual_columns.py", title="Virtual Columns"),
        st.Page("content/demos/cookbook/40_example_highlight_change.py", title="Highlight Changes"),
        st.Page("content/demos/cookbook/60_rich_cell_editor.py", title="Rich Cell Editor"),
        st.Page("content/demos/cookbook/70_nested_grids.py", title="Nested Grids"),
        st.Page("content/demos/cookbook/80_saving_columns_state.py", title="Saving Column State"),
        st.Page("content/demos/cookbook/81_Tooltips.py", title="Tooltips"),
        st.Page("content/demos/cookbook/82_Handling_Grid_events.py", title="Handling Grid Events"),
        st.Page("content/demos/cookbook/83_fetching_real_time_data.py", title="Real-time Data Fetching"),
        st.Page("content/demos/cookbook/99_one_billion_row.py", title="One Billion Rows"),
        st.Page("content/demos/cookbook/custom_css.py", title="Custom CSS"),
        st.Page("content/demos/cookbook/custom_tooltip.py", title="Custom Tooltips"),
        st.Page("content/demos/cookbook/forms.py", title="Forms Integration"),
        st.Page("content/demos/cookbook/gridOptions_playground.py", title="GridOptions Playground"),
        st.Page("content/demos/cookbook/json_data.py", title="JSON Data"),
        st.Page("content/demos/cookbook/native_grid_compare.py", title="Native Grid Comparison"),
        st.Page("content/demos/cookbook/polars_dataframe.py", title="Polars DataFrame"),
        st.Page("content/demos/cookbook/rowAdd.py", title="Row Addition"),
        st.Page("content/demos/cookbook/websocket.py", title="WebSocket Integration"),
    ]
}

# Inject UI components
#inject_banner_styles()
#render_banner()
render_premium_button()

st.navigation(pages, position="top").run()
