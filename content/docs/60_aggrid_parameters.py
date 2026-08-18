"""
AgGrid Parameters Reference
============================

Complete API documentation for AgGrid function parameters.
"""

import streamlit as st
from streamlit_aggrid import AgGrid, GridOptionsBuilder
from streamlit_aggrid.shared import DataReturnMode
import pandas as pd
import numpy as np

st.set_page_config(page_title="AgGrid Parameters", layout="wide")

# ============================================================================
# SECTION CONTROL - Set to True/False to enable/disable sections
# ============================================================================
SECTIONS = {
    'overview': True,
    'complete_example': True,
    'data': True,
    'gridOptions': True,
    'key': True,
    'height': True,
    'theme': True,
    'update_on': True,
    'data_return_mode': True,
    'callback': True,
    'enable_enterprise': True,
    'license_key': True,
    'toolbar': True,
    'allow_unsafe_jscode': True,
    'columns_state': True,
    'use_json_serialization': True,
    'server_sync_strategy': True,
    'isolate_styles': True,
}

# Sidebar navigation
with st.sidebar:
    st.markdown('''
    <div class="sidebar-nav-section">On this page</div>
    <div class="sidebar-nav-container">
        <a href="#overview" class="sidebar-nav-link">Overview</a>
        <a href="#complete-example" class="sidebar-nav-link">Example</a>
        <div class="sidebar-nav-section">Parameters</div>
        <a href="#data" class="sidebar-nav-link">data</a>
        <a href="#gridoptions" class="sidebar-nav-link">gridOptions</a>
        <a href="#key" class="sidebar-nav-link">key</a>
        <a href="#height" class="sidebar-nav-link">height</a>
        <a href="#theme" class="sidebar-nav-link">theme</a>
        <a href="#update-on" class="sidebar-nav-link">update_on</a>
        <a href="#data-return-mode" class="sidebar-nav-link">data_return_mode</a>
        <a href="#callback" class="sidebar-nav-link">callback</a>
        <a href="#enable-enterprise-modules" class="sidebar-nav-link">enable_enterprise_modules</a>
        <a href="#license-key" class="sidebar-nav-link">license_key</a>
        <a href="#toolbar-parameters" class="sidebar-nav-link">Toolbar Parameters</a>
        <a href="#allow-unsafe-jscode" class="sidebar-nav-link">allow_unsafe_jscode</a>
        <a href="#columns-state" class="sidebar-nav-link">columns_state</a>
        <a href="#use-json-serialization" class="sidebar-nav-link">use_json_serialization</a>
        <a href="#server-sync-strategy" class="sidebar-nav-link">server_sync_strategy</a>
        <a href="#isolate-styles" class="sidebar-nav-link">isolate_styles</a>
    </div>
    ''', unsafe_allow_html=True)

st.title("AgGrid Parameters Reference")

st.markdown("""
Complete reference for all `AgGrid()` function parameters.
""")


# ============================================================================
# SECTION FUNCTIONS
# ============================================================================

def section_overview():
    """Overview Section"""
    st.header("Overview", anchor="overview")

    st.markdown("""
    The `AgGrid` function renders a DataFrame as an interactive grid.

    ### Basic Signature

    ```python
    from streamlit_aggrid import AgGrid

    result = AgGrid(
        data,                    # Your DataFrame
        gridOptions=None,        # Grid configuration
        key=None,                # Streamlit widget key
        height=400,              # Grid height in pixels
        theme='streamlit',       # Visual theme
        update_on=[...],         # Events that trigger updates
        **kwargs                 # Additional options
    )
    ```
    """)


def section_complete_example():
    """Complete Example Section"""
    st.subheader("Complete Example", anchor="complete-example")

    st.markdown("""
    This example demonstrates common AgGrid parameters in use.
    """)

    # Create sample data
    np.random.seed(42)
    df = pd.DataFrame({
        'athlete': ['Michael Phelps', 'Natalie Coughlin', 'Aleksey Nemov',
                    'Alicia Coutts', 'Missy Franklin'] * 3,
        'age': np.random.randint(20, 35, 15),
        'country': ['United States', 'United States', 'Russia',
                    'Australia', 'United States'] * 3,
        'year': np.random.choice([2000, 2004, 2008, 2012], 15),
        'sport': ['Swimming', 'Swimming', 'Gymnastics',
                  'Swimming', 'Swimming'] * 3,
        'gold': np.random.randint(0, 10, 15),
        'silver': np.random.randint(0, 5, 15),
        'bronze': np.random.randint(0, 5, 15),
    })

    # Build grid options
    gb = GridOptionsBuilder.from_dataframe(df)
    gb.configure_default_column(resizable=True, filterable=True, sortable=True)
    gb.configure_selection('multiple', use_checkbox=True)
    gb.configure_column('athlete', pinned='left', width=200)
    gridOptions = gb.build()

    # Render grid
    result = AgGrid(
        df,
        gridOptions=gridOptions,
        height=350,
        theme='streamlit',
        update_on=['selectionChanged'],
        key='params_demo',
        data_return_mode=DataReturnMode.FILTERED_AND_SORTED,
    )

    # Show results
    if result.selected_data is not None and len(result.selected_data) > 0:
        st.success(f"Selected {len(result.selected_data)} rows")

    with st.expander("Show code", expanded=False):
        st.code("""
from streamlit_aggrid import AgGrid, GridOptionsBuilder
from streamlit_aggrid.shared import DataReturnMode

# Configure grid
gb = GridOptionsBuilder.from_dataframe(df)
gb.configure_default_column(resizable=True, filterable=True)
gb.configure_selection('multiple', use_checkbox=True)
gridOptions = gb.build()

# Render
result = AgGrid(
    df,
    gridOptions=gridOptions,
    height=350,
    theme='streamlit',
    update_on=['selectionChanged'],
    key='my_grid',
    data_return_mode=DataReturnMode.FILTERED_AND_SORTED,
)
""", language="python")

    st.divider()


def section_data():
    """data parameter"""
    st.header("data", anchor="data")

    st.code("""
data: pd.DataFrame | pl.DataFrame | str | Path | None = None
""", language="python")

    st.markdown("""
    The data to display in the grid.

    **Accepted types:**
    - `pd.DataFrame` - Pandas DataFrame (most common)
    - `pl.DataFrame` - Polars DataFrame
    - `str` - JSON string in records format
    - `Path` - Path to JSON file
    - `None` - Empty grid

    **Example:**
    ```python
    # Pandas DataFrame
    df = pd.DataFrame({'name': ['Alice', 'Bob'], 'age': [25, 30]})
    AgGrid(df)

    # Polars DataFrame
    import polars as pl
    pl_df = pl.DataFrame({'name': ['Alice', 'Bob'], 'age': [25, 30]})
    AgGrid(pl_df)

    # JSON string
    json_data = '[{"name": "Alice", "age": 25}, {"name": "Bob", "age": 30}]'
    AgGrid(json_data)
    ```
    """)


def section_gridOptions():
    """gridOptions parameter"""
    st.header("gridOptions", anchor="gridoptions")

    st.code("""
gridOptions: dict | None = None
""", language="python")

    st.markdown("""
    AG Grid configuration dictionary.

    **If None:** Default options are inferred from the DataFrame.

    **Recommended:** Use `GridOptionsBuilder` to build gridOptions.

    **Example:**
    ```python
    from streamlit_aggrid import GridOptionsBuilder

    gb = GridOptionsBuilder.from_dataframe(df)
    gb.configure_default_column(resizable=True, filterable=True)
    gb.configure_selection('multiple')
    gridOptions = gb.build()

    AgGrid(df, gridOptions=gridOptions)
    ```

    See [GridOptionsBuilder](30_grid_options_builder) and [AG Grid Options](https://www.ag-grid.com/javascript-data-grid/grid-options/).
    """)


def section_key():
    """key parameter"""
    st.header("key", anchor="key")

    st.code("""
key: Any | None = None
""", language="python")

    st.markdown("""
    Streamlit widget key for state management.

    **Highly recommended** to set a unique key for each grid.

    **Example:**
    ```python
    # Single grid
    result = AgGrid(df, key='my_grid')

    # Multiple grids
    col1, col2 = st.columns(2)
    with col1:
        result1 = AgGrid(df1, key='grid_1')
    with col2:
        result2 = AgGrid(df2, key='grid_2')
    ```
    """)


def section_height():
    """height parameter"""
    st.header("height", anchor="height")

    st.code("""
height: int | None = 400
""", language="python")

    st.markdown("""
    Grid height in pixels.

    **Values:**
    - `int` - Fixed height (e.g., 400, 600)
    - `None` - Auto height (shows all rows, no scroll)

    **Example:**
    ```python
    # Fixed height
    AgGrid(df, height=500)

    # Auto height
    AgGrid(df, height=None)

    # Dynamic height
    calculated_height = min(len(df) * 35 + 50, 600)
    AgGrid(df, height=calculated_height)
    ```
    """)


def section_theme():
    """theme parameter"""
    st.header("theme", anchor="theme")

    st.code("""
theme: str = 'streamlit'
""", language="python")

    st.markdown("""
    Visual theme for the grid.

    **Available themes:**
    - `'streamlit'` - Matches Streamlit styling (recommended)
    - `'light'` - AG Grid balham-light
    - `'dark'` - AG Grid balham-dark
    - `'blue'` - AG Grid blue
    - `'fresh'` - AG Grid fresh
    - `'material'` - AG Grid material

    **Example:**
    ```python
    AgGrid(df, theme='streamlit')  # Default
    AgGrid(df, theme='dark')
    AgGrid(df, theme='material')
    ```

    See [AG Grid Themes](https://www.ag-grid.com/javascript-data-grid/themes/).
    """)


def section_update_on():
    """update_on parameter"""
    st.header("update_on", anchor="update-on")

    st.code("""
update_on: list[str | tuple[str, int]] = [
    'cellValueChanged',
    'selectionChanged',
    'filterChanged',
    'sortChanged'
]
""", language="python")

    st.markdown("""
    AG Grid events that trigger Streamlit reruns.

    **Format:**
    - `str` - Event name
    - `tuple[str, int]` - Event name with debounce (milliseconds)

    **Common events:**
    - `'selectionChanged'` - Row selection changed
    - `'cellValueChanged'` - Cell edited
    - `'filterChanged'` - Filter applied/removed
    - `'sortChanged'` - Sort order changed
    - `'columnResized'` - Column width changed

    **Example:**
    ```python
    # Only update on selection
    AgGrid(df, update_on=['selectionChanged'])

    # Multiple events
    AgGrid(df, update_on=['selectionChanged', 'cellValueChanged'])

    # With debouncing (wait 500ms after last event)
    AgGrid(df, update_on=[
        'selectionChanged',
        ('columnResized', 500),
        ('filterChanged', 300),
    ])

    # No automatic updates
    AgGrid(df, update_on=[])
    ```

    See [AG Grid Events](https://www.ag-grid.com/javascript-data-grid/grid-events/).
    """)


def section_data_return_mode():
    """data_return_mode parameter"""
    st.header("data_return_mode", anchor="data-return-mode")

    st.code("""
data_return_mode: DataReturnMode | str = DataReturnMode.FILTERED_AND_SORTED
""", language="python")

    st.markdown("""
    Controls what data is returned in `result.data`.

    **Modes:**
    - `AS_INPUT` - All rows as originally provided
    - `FILTERED` - Only rows matching current filters
    - `FILTERED_AND_SORTED` - Filtered rows in current sort order (default)

    **Example:**
    ```python
    from streamlit_aggrid.shared import DataReturnMode

    # Return all data
    result = AgGrid(df, data_return_mode=DataReturnMode.AS_INPUT)

    # Return filtered data
    result = AgGrid(df, data_return_mode=DataReturnMode.FILTERED)

    # Return filtered and sorted (default)
    result = AgGrid(df, data_return_mode=DataReturnMode.FILTERED_AND_SORTED)

    # Can use strings
    result = AgGrid(df, data_return_mode='FILTERED')
    ```
    """)


def section_callback():
    """callback parameter"""
    st.header("callback", anchor="callback")

    st.code("""
callback: callable | None = None
""", language="python")

    st.markdown("""
    Function called when grid data changes.

    **Requirements:**
    - Must set `key` parameter
    - Function receives `AgGridReturn` object

    **Example:**
    ```python
    def on_grid_change(grid_return):
        if grid_return.selected_data is not None:
            st.write(f"Selected {len(grid_return.selected_data)} rows")

    AgGrid(df, key='my_grid', callback=on_grid_change)
    ```

    **With session state:**
    ```python
    def save_selection(grid_return):
        if grid_return.selected_data is not None:
            st.session_state['selection'] = grid_return.selected_data

    AgGrid(df, key='grid', callback=save_selection)
    ```
    """)


def section_enable_enterprise():
    """enable_enterprise_modules parameter"""
    st.header("enable_enterprise_modules", anchor="enable-enterprise-modules")

    st.code("""
enable_enterprise_modules: bool | Literal['enterpriseOnly', 'enterprise+AgCharts'] = False
""", language="python")

    st.markdown("""
    Enable AG Grid Enterprise features (requires license).

    **Values:**
    - `False` - Community features only (default)
    - `True` or `'enterpriseOnly'` - Enterprise features
    - `'enterprise+AgCharts'` - Enterprise + AgCharts

    **Enterprise features:**
    - Row grouping and aggregation
    - Tree data
    - Server-side row model
    - Advanced filtering
    - Excel export
    - Range selection

    **Example:**
    ```python
    # Enable enterprise
    AgGrid(
        df,
        gridOptions=gridOptions,
        enable_enterprise_modules=True,
        license_key='YOUR_LICENSE_KEY'
    )

    # Row grouping example
    gb = GridOptionsBuilder.from_dataframe(df)
    gb.configure_column('country', rowGroup=True)
    gb.configure_column('sport', rowGroup=True)
    gridOptions = gb.build()

    AgGrid(df, gridOptions=gridOptions, enable_enterprise_modules=True)
    ```

    See [AG Grid Enterprise](https://www.ag-grid.com/javascript-data-grid/licensing/).
    """)


def section_license_key():
    """license_key parameter"""
    st.header("license_key", anchor="license-key")

    st.code("""
license_key: str | None = None
""", language="python")

    st.markdown("""
    AG Grid Enterprise license key.

    **Example:**
    ```python
    AgGrid(
        df,
        enable_enterprise_modules=True,
        license_key='YOUR_LICENSE_KEY_HERE'
    )
    ```

    Get a license at [AG Grid Pricing](https://www.ag-grid.com/license-pricing/).
    """)


def section_toolbar():
    """Toolbar parameters"""
    st.header("Toolbar Parameters", anchor="toolbar-parameters")

    st.code("""
show_toolbar: bool = True
show_search: bool = True
show_download_button: bool = True
""", language="python")

    st.markdown("""
    Control toolbar visibility and features.

    **Example:**
    ```python
    # Default - show all
    AgGrid(df, show_toolbar=True, show_search=True, show_download_button=True)

    # Hide toolbar
    AgGrid(df, show_toolbar=False)

    # Show toolbar without search
    AgGrid(df, show_toolbar=True, show_search=False)
    ```
    """)


def section_allow_unsafe_jscode():
    """allow_unsafe_jscode parameter"""
    st.header("allow_unsafe_jscode", anchor="allow-unsafe-jscode")

    st.code("""
allow_unsafe_jscode: bool = False
""", language="python")

    st.markdown("""
    Allow JavaScript code injection via `JsCode` objects.

    **Required when using:**
    - Custom cell renderers
    - Custom value getters/setters
    - Custom filters

    **Example:**
    ```python
    from streamlit_aggrid.shared import JsCode

    cell_renderer = JsCode('''
        function(params) {
            return '<b>' + params.value + '</b>';
        }
    ''')

    gb = GridOptionsBuilder.from_dataframe(df)
    gb.configure_column('athlete', cellRenderer=cell_renderer)
    gridOptions = gb.build()

    AgGrid(df, gridOptions=gridOptions, allow_unsafe_jscode=True)
    ```

    **Security:** Only enable for trusted JavaScript code.
    """)


def section_columns_state():
    """columns_state parameter"""
    st.header("columns_state", anchor="columns-state")

    st.code("""
columns_state: dict | None = None
""", language="python")

    st.markdown("""
    Initial column state (visibility, order, width, pinning).

    **Example:**
    ```python
    # Save column state
    result = AgGrid(df, key='my_grid')
    if result.columns_state:
        st.session_state['saved_columns'] = result.columns_state

    # Restore column state
    AgGrid(
        df,
        columns_state=st.session_state.get('saved_columns'),
        key='my_grid'
    )
    ```

    See [Column State API](https://www.ag-grid.com/javascript-data-grid/column-state/).
    """)


def section_use_json_serialization():
    """use_json_serialization parameter"""
    st.header("use_json_serialization", anchor="use-json-serialization")

    st.code("""
use_json_serialization: bool | Literal['auto'] = 'auto'
""", language="python")

    st.markdown("""
    Control JSON serialization for complex data types (lists, dicts, sets).

    **Values:**
    - `'auto'` - Auto-detect PyArrow errors and retry with JSON (default)
    - `True` - Always use JSON serialization
    - `False` - Never use JSON (raises error on non-hashable data)

    **Example:**
    ```python
    # DataFrame with complex types
    df = pd.DataFrame({
        'name': ['Alice', 'Bob'],
        'tags': [['python', 'data'], ['javascript', 'web']],
        'metadata': [{'role': 'dev'}, {'role': 'designer'}]
    })

    # Auto-detect (recommended)
    AgGrid(df, use_json_serialization='auto')

    # Force JSON
    AgGrid(df, use_json_serialization=True)
    ```
    """)


def section_server_sync_strategy():
    """server_sync_strategy parameter"""
    st.header("server_sync_strategy", anchor="server-sync-strategy")

    st.code("""
server_sync_strategy: Literal['client_wins', 'server_wins'] = 'client_wins'
""", language="python")

    st.markdown("""
    Control data synchronization between server and client.

    **Values:**
    - `'client_wins'` - Grid maintains local edits (default)
    - `'server_wins'` - Server data always overwrites grid

    **Example:**
    ```python
    # Standard editing (edits preserved)
    AgGrid(df, server_sync_strategy='client_wins')

    # Server as source of truth
    AgGrid(df, server_sync_strategy='server_wins')

    # Preserve edits with server_wins
    if 'grid_data' not in st.session_state:
        st.session_state['grid_data'] = df

    result = AgGrid(
        st.session_state['grid_data'],
        server_sync_strategy='server_wins'
    )

    if result.data is not None:
        st.session_state['grid_data'] = result.data
    ```
    """)


def section_isolate_styles():
    """isolate_styles parameter"""
    st.header("isolate_styles", anchor="isolate-styles")

    st.code("""
isolate_styles: bool = True
""", language="python")

    st.markdown("""
    Isolate component styles in shadow DOM.

    **Values:**
    - `True` - Styles isolated (default)
    - `False` - Allows CSS injection via `st.markdown()`

    **Example:**
    ```python
    # Inject custom CSS
    from streamlit_aggrid.styles import get_hide_expanders_css

    st.markdown(get_hide_expanders_css(), unsafe_allow_html=True)

    # Must disable isolation
    AgGrid(df, isolate_styles=False)
    ```
    """)


# ============================================================================
# RENDER SECTIONS
# ============================================================================

if SECTIONS.get('overview'):
    section_overview()

if SECTIONS.get('complete_example'):
    section_complete_example()

st.title("Parameters", anchor='parameters')

if SECTIONS.get('data'):
    section_data()

if SECTIONS.get('gridOptions'):
    section_gridOptions()

if SECTIONS.get('key'):
    section_key()

if SECTIONS.get('height'):
    section_height()

if SECTIONS.get('theme'):
    section_theme()

if SECTIONS.get('update_on'):
    section_update_on()

if SECTIONS.get('data_return_mode'):
    section_data_return_mode()

if SECTIONS.get('callback'):
    section_callback()

if SECTIONS.get('enable_enterprise'):
    section_enable_enterprise()

if SECTIONS.get('license_key'):
    section_license_key()

if SECTIONS.get('toolbar'):
    section_toolbar()

if SECTIONS.get('allow_unsafe_jscode'):
    section_allow_unsafe_jscode()

if SECTIONS.get('columns_state'):
    section_columns_state()

if SECTIONS.get('use_json_serialization'):
    section_use_json_serialization()

if SECTIONS.get('server_sync_strategy'):
    section_server_sync_strategy()

if SECTIONS.get('isolate_styles'):
    section_isolate_styles()


# ============================================================================
# FOOTER
# ============================================================================

st.divider()

st.info("""
**Learn More:**

- [AG Grid Options](https://www.ag-grid.com/javascript-data-grid/grid-options/)
- [AG Grid Events](https://www.ag-grid.com/javascript-data-grid/grid-events/)
- [GridOptionsBuilder](30_grid_options_builder)
- [AgGridReturn API](45_AgGridReturn)
""")
