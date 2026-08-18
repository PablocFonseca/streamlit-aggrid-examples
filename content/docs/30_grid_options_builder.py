"""
GridOptionsBuilder API Reference
=================================

API documentation for GridOptionsBuilder methods with MultiIndex example.
"""

import streamlit as st
from streamlit_aggrid import AgGrid, GridOptionsBuilder 
import pandas as pd
import numpy as np

st.set_page_config(page_title="GridOptionsBuilder API", layout="wide")

# ============================================================================
# SECTION CONTROL - Set to True/False to enable/disable sections
# ============================================================================
SECTIONS = {
    'overview': True,
    'complete_example': True,
    'from_dataframe': True,
    'configure_column': True,
    'configure_default_column': True,
    'configure_selection': True,
    'configure_pagination': True,
    'configure_side_bar': True,
    'configure_grid_options': True,
    'build': True,
}

# Sidebar navigation
with st.sidebar:
    st.markdown('''
    <div class="sidebar-nav-section">On this page</div>
    <div class="sidebar-nav-container">
        <a href="#overview" class="sidebar-nav-link">Overview</a>
        <a href="#complete-example" class="sidebar-nav-link">Example</a>
        <div class="sidebar-nav-section" style="text-transform: none !important"><span style="text-transform: capitalize">GridOptionsBuilder API</span></div>
        <a href="#from-dataframe" class="sidebar-nav-link">from_dataframe()</a>
        <a href="#configure-column" class="sidebar-nav-link">configure_column()</a>
        <a href="#configure-default-column" class="sidebar-nav-link">configure_default_column()</a>
        <a href="#configure-selection" class="sidebar-nav-link">configure_selection()</a>
        <a href="#configure-pagination" class="sidebar-nav-link">configure_pagination()</a>
        <a href="#configure-side-bar" class="sidebar-nav-link">configure_side_bar()</a>
        <a href="#configure-grid-options" class="sidebar-nav-link">configure_grid_options()</a>
        <a href="#build" class="sidebar-nav-link">build()</a>
    </div>
    ''', unsafe_allow_html=True)

st.title("GridOptionsBuilder API Reference")

st.markdown("""
Complete API documentation for GridOptionsBuilder methods.
Use GridOptionsBuilder to programmatically configure AG Grid options.
""")


# ============================================================================
# SECTION FUNCTIONS
# ============================================================================

def section_overview():
    """Overview Section"""
    st.header("Overview", anchor="overview")

    st.markdown("""
    `GridOptionsBuilder` provides a fluent API for building AG Grid configuration. It automatically
    infers the best grid layout from your DataFrame structure, including:

    - **Column types and formatting** - Automatically detects numeric, text, date columns
    - **MultiIndex columns** - Creates nested column groups with collapsible hierarchies
    - **MultiIndex rows** - Sets up row grouping with proper display columns
    - **Default behaviors** - Applies sensible defaults (resizable, sortable, filterable)

    ### Basic Usage

    ```python
    from streamlit_aggrid import GridOptionsBuilder

    gb = GridOptionsBuilder.from_dataframe(df)
    gb.configure_default_column(resizable=True, filterable=True)
    gb.configure_selection('multiple', use_checkbox=True)
    gridOptions = gb.build()
    ```
    """)


def section_complete_example():
    """Complete Example Section"""
    st.subheader("Complete Example: Automatic Layout Inference", anchor="complete-example")

    st.markdown("""
    The example below demonstrates automatic inference with a complex MultiIndex DataFrame
    containing both hierarchical columns (Sales/Profit → Quarters → Months) and row groups
    (Region → Product → Color).

    **Try these interactions:**
    - **Expand/collapse column groups** - Click the arrow icons in the column headers to show/hide nested columns
    - **Expand/collapse row groups** - Click the arrow icons in rows to drill down from Region → Product → Color
    - **Resize columns** - Drag column borders to adjust widths
    - **Hover over group icons** - Notice how expand/collapse icons appear only on hover for a cleaner look

    All of this functionality is automatically configured by `GridOptionsBuilder` based on your DataFrame structure!
    """)

    # Create MultiIndex DataFrame
    np.random.seed(42)

    columns = pd.MultiIndex.from_product(
        [['Sales', 'Profit'], ['Q1', 'Q2', 'Q3', 'Q4'], ['M1', 'M2']],
        names=['Metric', 'Quarter', 'Half']
    )

    index = pd.MultiIndex.from_product(
        [['North', 'South'], ['Product A', 'Product B', 'Product C'], ['Blue', 'Red']],
        names=['Region', 'Product', 'Color']
    )

    data = np.random.randint(100, 1000, size=(len(index), len(columns)))
    df = pd.DataFrame(data, index=index, columns=columns)


    # Build grid
    gb = GridOptionsBuilder.from_dataframe(df, parse_multi_index=True)
    gb.configure_default_column(resizable=True, filterable=True, sortable=True)

    df_reset = df.reset_index()
    first_data_col = str(df_reset.columns[3])
    gb.configure_column(first_data_col, checkboxSelection=True, headerCheckboxSelection=True)

    gb.configure_grid_options(
        rowSelection='multiple',
        suppressRowClickSelection=True
    )

    gridOptions = gb.build()
    result = AgGrid(
        df_reset,
        gridOptions=gridOptions,
        height=500,
        theme='streamlit',
        enable_enterprise_modules=True,
        key='multiindex_demo',
        isolate_styles=False
    )

    # Show selection
    if result.selected_rows is not None and len(result.selected_rows) > 0:
        st.success(f"Selected {len(result.selected_rows)} rows")
        with st.expander("View selected rows"):
            st.dataframe(pd.DataFrame(result.selected_rows))

    with st.expander("Show code", expanded=False):
        st.code("""
from streamlit_aggrid import AgGrid, GridOptionsBuilder, get_hide_expanders_css
import streamlit as st
import pandas as pd
import numpy as np

# Create MultiIndex DataFrame
columns = pd.MultiIndex.from_product(
    [['Sales', 'Profit'], ['Q1', 'Q2', 'Q3', 'Q4'], ['M1', 'M2']],
    names=['Metric', 'Quarter', 'Half']
)

index = pd.MultiIndex.from_product(
    [['North', 'South'], ['Product A', 'Product B', 'Product C'], ['Blue', 'Red']],
    names=['Region', 'Product', 'Color']
)

data = np.random.randint(100, 1000, size=(len(index), len(columns)))
df = pd.DataFrame(data, index=index, columns=columns)

# Hide expand icons until hover (optional)
st.markdown(get_hide_expanders_css(), unsafe_allow_html=True)

# Build grid options with MultiIndex parsing
gb = GridOptionsBuilder.from_dataframe(df, parse_multi_index=True)

# Configure defaults
gb.configure_default_column(resizable=True, filterable=True, sortable=True)

# Configure selection
df_reset = df.reset_index()
first_data_col = str(df_reset.columns[3])
gb.configure_column(first_data_col, checkboxSelection=True, headerCheckboxSelection=True)

gb.configure_grid_options(
    rowSelection='multiple',
    suppressRowClickSelection=True
)

# Build and render
gridOptions = gb.build()
result = AgGrid(
    df_reset,
    gridOptions=gridOptions,
    height=500,
    theme='streamlit',
    enable_enterprise_modules=True, #for row grouping
    isolate_styles=False #allows css injection via st.markdown
)

# Show selected rows
if result.selected_rows is not None and len(result.selected_rows) > 0:
    st.write(f"Selected {len(result.selected_rows)} rows")
    st.dataframe(pd.DataFrame(result.selected_rows))
""", language="python")

    st.divider()


def section_api_header():
    """API Header"""
    st.title("GridOptionsBuilder API", anchor='gridoptionsbuilder-api')


def section_from_dataframe():
    """from_dataframe() API"""
    st.header("from_dataframe()", anchor="from-dataframe")

    st.code("""
@staticmethod
GridOptionsBuilder.from_dataframe(
    dataframe: pd.DataFrame | pl.DataFrame,
    parse_multi_index: bool = False,
    multi_index_column_groups_open: bool = True,
    **default_column_parameters,
) -> GridOptionsBuilder
""", language="python")

    st.markdown("""
    Creates a GridOptionsBuilder instance from a DataFrame. Column definitions are automatically
    created based on DataFrame columns and data types.

    **Parameters:**
    - `dataframe` (pd.DataFrame | pl.DataFrame): Pandas or Polars DataFrame
    - `parse_multi_index` (bool): If True, creates column groups from MultiIndex columns and row groups
      from MultiIndex index. Requires AG Grid Enterprise. Default: False
    - `multi_index_column_groups_open` (bool): If True, column groups created from MultiIndex columns
      will be open by default. If False, they will be closed by default. Only applies when
      parse_multi_index=True. Default: True
    - `**default_column_parameters`: Additional parameters for default column configuration

    **Returns:**
    - GridOptionsBuilder: Instance initialized from the DataFrame

    **Example:**
    ```python
    # Basic usage
    gb = GridOptionsBuilder.from_dataframe(df)

    # With MultiIndex support (groups open by default)
    gb = GridOptionsBuilder.from_dataframe(df, parse_multi_index=True)

    # With MultiIndex support (groups closed by default)
    gb = GridOptionsBuilder.from_dataframe(df, parse_multi_index=True, multi_index_column_groups_open=False)

    # With default parameters
    gb = GridOptionsBuilder.from_dataframe(df, resizable=True, sortable=True)
    ```
    """)


def section_configure_column():
    """configure_column() API"""
    st.header("configure_column()", anchor="configure-column")

    st.code("""
configure_column(
    field: str | list[str] | None = None,
    header_name: str | None = None,
    col_id: str | None = None,
    children: list[str] | None = None,
    **other_column_properties,
) -> GridOptionsBuilder
""", language="python")

    st.markdown("""
    Configures one or multiple columns.

    This method can configure:
    1. **Regular columns**: Have a 'field' that maps to data
    2. **Virtual columns**: No 'field', use 'valueGetter' to compute values
    3. **Column groups**: No 'field', have 'children' list to group other columns
    4. **Batch configuration**: Pass a list of field names to apply same properties to multiple columns

    **Parameters:**
    - `field` (str | list[str]): Field name(s) from data. If a list, applies properties to all fields (batch mode).
      If a string, configures single column. Omit for virtual columns and groups
    - `header_name` (str): Display name in column header (single column mode only)
    - `col_id` (str): Explicit unique identifier. Auto-generated if not provided (single column mode only)
    - `children` (list[str]): List of colIds (field names) to group. Makes this a column group
    - `**other_column_properties`: Any AG Grid column properties (width, pinned, valueGetter, etc.)

    **Examples:**
    ```python
    # Regular column
    gb.configure_column('price', header_name='Unit Price', width=150)

    # Batch configuration (multiple columns)
    gb.configure_column(['age', 'year'], width=80, filterable=False)
    gb.configure_column(['id', 'internal_code'], hide=True)

    # Column group
    gb.configure_column(header_name='Athlete Info', children=['name', 'age', 'country'])

    # With formatting
    gb.configure_column('total', valueFormatter="value >= 5 ? '🏆 ' + value : value")
    ```

    See [AG Grid Column Properties](https://www.ag-grid.com/javascript-data-grid/column-properties/) for all available properties.
    """)


def section_configure_default_column():
    """configure_default_column() API"""
    st.header("configure_default_column()", anchor="configure-default-column")

    st.code("""
configure_default_column(
    **other_default_column_properties,
) -> GridOptionsBuilder
""", language="python")

    st.markdown("""
    Configure default properties for all columns.

    **Common Parameters:**
    - `resizable` (bool): Allow column resizing
    - `sortable` (bool): Enable sorting
    - `filterable` or `filter` (bool): Enable filtering
    - `editable` (bool): Allow cell editing
    - `minWidth` (int): Minimum column width
    - `maxWidth` (int): Maximum column width
    - `width` (int): Default column width

    **Example:**
    ```python
    gb.configure_default_column(
        resizable=True,
        sortable=True,
        filterable=True,
        minWidth=100
    )
    ```
    """)


def section_configure_selection():
    """configure_selection() API"""
    st.header("configure_selection()", anchor="configure-selection")

    st.code("""
configure_selection(
    selection_mode: str = 'single',
    use_checkbox: bool = False,
    header_checkbox: bool = False,
    header_checkbox_filtered_only: bool = True,
    pre_select_all_rows: bool = False,
    pre_selected_rows: list[int] | None = None,
    rowMultiSelectWithClick: bool = False,
    suppressRowDeselection: bool = False,
    suppressRowClickSelection: bool = False,
    groupSelectsChildren: bool = True,
    groupSelectsFiltered: bool = True,
) -> GridOptionsBuilder
""", language="python")

    st.markdown("""
    Configure grid selection features.

    **Parameters:**
    - `selection_mode` (str): 'single', 'multiple', or 'disabled'
    - `use_checkbox` (bool): Add checkbox column for selection
    - `header_checkbox` (bool): Add select-all checkbox in header
    - `header_checkbox_filtered_only` (bool): Select-all only selects filtered rows
    - `pre_select_all_rows` (bool): Pre-select all rows on load
    - `pre_selected_rows` (list): List of row indices to pre-select
    - `rowMultiSelectWithClick` (bool): Click to toggle selection (no Ctrl/Shift needed)
    - `suppressRowDeselection` (bool): Prevent deselecting rows
    - `suppressRowClickSelection` (bool): Only checkbox can select (not row clicks)
    - `groupSelectsChildren` (bool): Selecting group selects all children
    - `groupSelectsFiltered` (bool): Group selection respects filters

    **Example:**
    ```python
    # Multiple selection with checkboxes
    gb.configure_selection(
        selection_mode='multiple',
        use_checkbox=True,
        header_checkbox=True,
        suppressRowClickSelection=True
    )
    ```
    """)


def section_configure_pagination():
    """configure_pagination() API"""
    st.header("configure_pagination()", anchor="configure-pagination")

    st.code("""
configure_pagination(
    enabled: bool = True,
    paginationAutoPageSize: bool = True,
    paginationPageSize: int = 10,
) -> GridOptionsBuilder
""", language="python")

    st.markdown("""
    Configure grid pagination features.

    **Parameters:**
    - `enabled` (bool): Enable pagination
    - `paginationAutoPageSize` (bool): Calculate page size from grid height
    - `paginationPageSize` (int): Rows per page (when auto-size is False)

    **Example:**
    ```python
    # Auto page size
    gb.configure_pagination(enabled=True, paginationAutoPageSize=True)

    # Fixed page size
    gb.configure_pagination(enabled=True, paginationPageSize=50)
    ```
    """)


def section_configure_side_bar():
    """configure_side_bar() API"""
    st.header("configure_side_bar()", anchor="configure-side-bar")

    st.code("""
configure_side_bar(
    filters_panel: bool = True,
    columns_panel: bool = True,
    defaultToolPanel: str = '',
) -> GridOptionsBuilder
""", language="python")

    st.markdown("""
    Configure side panel tool panels. Enterprise feature.

    **Parameters:**
    - `filters_panel` (bool): Enable filters panel
    - `columns_panel` (bool): Enable columns panel
    - `defaultToolPanel` (str): Panel to open by default ('filters', 'columns', or '')

    **Example:**
    ```python
    gb.configure_side_bar(
        filters_panel=True,
        columns_panel=True,
        defaultToolPanel='filters'
    )
    ```
    """)


def section_configure_grid_options():
    """configure_grid_options() API"""
    st.header("configure_grid_options()", anchor="configure-grid-options")

    st.code("""
configure_grid_options(
    **props,
) -> GridOptionsBuilder
""", language="python")

    st.markdown("""
    Merge properties directly to gridOptions root. Use this to set any AG Grid option.

    **Parameters:**
    - `**props`: Any AG Grid grid options

    **Example:**
    ```python
    gb.configure_grid_options(
        animateRows=True,
        rowHeight=35,
        enableRangeSelection=True,
        suppressMovableColumns=False
    )
    ```

    See [AG Grid Options](https://www.ag-grid.com/javascript-data-grid/grid-options/) for all available options.
    """)


def section_build():
    """build() API"""
    st.header("build()", anchor="build")

    st.code("""
build() -> dict
""", language="python")

    st.markdown("""
    Build and return the final gridOptions dictionary.

    **Returns:**
    - dict: GridOptions dictionary ready for AgGrid component

    **Example:**
    ```python
    gb = GridOptionsBuilder.from_dataframe(df)
    gb.configure_default_column(resizable=True)
    gridOptions = gb.build()

    AgGrid(df, gridOptions=gridOptions)
    ```
    """)


# ============================================================================
# RENDER SECTIONS BASED ON CONFIGURATION
# ============================================================================

if SECTIONS.get('overview', False):
    section_overview()

if SECTIONS.get('complete_example', False):
    section_complete_example()

# API Header
section_api_header()

if SECTIONS.get('from_dataframe', False):
    section_from_dataframe()

if SECTIONS.get('configure_column', False):
    section_configure_column()

if SECTIONS.get('configure_default_column', False):
    section_configure_default_column()

if SECTIONS.get('configure_selection', False):
    section_configure_selection()

if SECTIONS.get('configure_pagination', False):
    section_configure_pagination()

if SECTIONS.get('configure_side_bar', False):
    section_configure_side_bar()

if SECTIONS.get('configure_grid_options', False):
    section_configure_grid_options()

if SECTIONS.get('build', False):
    section_build()


# ============================================================================
# FOOTER
# ============================================================================

st.divider()

st.info("""
**Learn More:**

- [AG Grid Grid Options](https://www.ag-grid.com/javascript-data-grid/grid-options/)
- [AG Grid Column Properties](https://www.ag-grid.com/javascript-data-grid/column-properties/)
- [AG Grid Row Grouping](https://www.ag-grid.com/javascript-data-grid/grouping/) (Enterprise)

Check out other documentation pages for detailed examples on column configuration, filtering, and editing.
""")
