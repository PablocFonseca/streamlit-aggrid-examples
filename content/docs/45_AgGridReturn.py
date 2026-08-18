"""
AgGridReturn API Reference
===========================

API documentation for AgGridReturn - the response object returned by the AgGrid component.
"""

import streamlit as st
from streamlit_aggrid import AgGrid, GridOptionsBuilder
import pandas as pd
import numpy as np

st.set_page_config(page_title="AgGridReturn API", layout="wide")

# ============================================================================
# SECTION CONTROL - Set to True/False to enable/disable sections
# ============================================================================
SECTIONS = {
    'overview': True,
    'complete_example': True,
    'data': True,
    'selected_data': True,
    'dataGroups': True,
    'grid_state': True,
    'columns_state': True,
    'event_data': True,
}

# Sidebar navigation
with st.sidebar:
    st.markdown('''
    <div class="sidebar-nav-section">On this page</div>
    <div class="sidebar-nav-container">
        <a href="#overview" class="sidebar-nav-link">Overview</a>
        <a href="#complete-example" class="sidebar-nav-link">Example</a>
        <div class="sidebar-nav-section" style="text-transform: none !important"><span style="text-transform: capitalize">AgGridReturn API</span></div>
        <a href="#data" class="sidebar-nav-link">data</a>
        <a href="#selected-data" class="sidebar-nav-link">selected_data</a>
        <a href="#datagroups" class="sidebar-nav-link">dataGroups</a>
        <a href="#grid-state" class="sidebar-nav-link">grid_state</a>
        <a href="#columns-state" class="sidebar-nav-link">columns_state</a>
        <a href="#event-data" class="sidebar-nav-link">event_data</a>
    </div>
    ''', unsafe_allow_html=True)

st.title("AgGridReturn API Reference")

st.markdown("""
Complete API documentation for the AgGridReturn object returned by the AgGrid component.
Use AgGridReturn to access grid data, selections, state, and user interactions.
""")


# ============================================================================
# SECTION FUNCTIONS
# ============================================================================

def section_overview():
    """Overview Section"""
    st.header("Overview", anchor="overview")

    st.markdown("""
    `AgGridReturn` is a container object returned by the `AgGrid()` component. It provides easy access to:

    - **Grid data** - All rows, filtered rows, or selected rows
    - **Grouped data** - Access data organized by row groups
    - **Grid state** - Column state, filter state, sort state
    - **User interactions** - Events and selections

    ### Basic Usage

    ```python
    from streamlit_aggrid import AgGrid

    result = AgGrid(df)

    # Access all data
    all_data = result.data

    # Access selected rows
    selected = result.selected_data

    # Access grid state
    state = result.grid_state
    ```

    ### Data Return Modes

    The AgGrid component accepts a `data_return_mode` parameter that controls how data is returned:

    - `AS_INPUT` (default) - Returns all rows as they were input
    - `FILTERED` - Returns only rows that pass the current filter
    - `FILTERED_AND_SORTED` - Returns filtered rows in their current sort order

    ```python
    from streamlit_aggrid.shared import DataReturnMode

    result = AgGrid(df, data_return_mode=DataReturnMode.FILTERED_AND_SORTED)
    ```
    """)


def section_complete_example():
    """Complete Example Section"""
    st.subheader("Complete Example: Working with AgGridReturn", anchor="complete-example")

    st.markdown("""
    This example demonstrates accessing data and selections from the AgGridReturn object.

    **Try these interactions:**
    - **Select rows** - Click checkboxes to select rows
    - **Filter data** - Use column filters to narrow results
    - **Sort columns** - Click headers to sort
    - **View results** - See how the return object captures your interactions
    """)

    # Create sample data
    np.random.seed(42)
    df = pd.DataFrame({
        'athlete': ['Michael Phelps', 'Natalie Coughlin', 'Aleksey Nemov',
                    'Alicia Coutts', 'Missy Franklin'] * 4,
        'age': np.random.randint(20, 35, 20),
        'country': ['United States', 'United States', 'Russia',
                    'Australia', 'United States'] * 4,
        'sport': ['Swimming', 'Swimming', 'Gymnastics',
                  'Swimming', 'Swimming'] * 4,
        'gold': np.random.randint(0, 10, 20),
        'silver': np.random.randint(0, 5, 20),
        'bronze': np.random.randint(0, 5, 20),
    })

    # Build grid options
    gb = GridOptionsBuilder.from_dataframe(df)
    gb.configure_default_column(resizable=True, filterable=True, sortable=True)
    gb.configure_selection(
        selection_mode='multiple',
        use_checkbox=True,
        header_checkbox=True
    )
    gb.configure_column('athlete', pinned='left', width=200)

    gridOptions = gb.build()

    # Render grid
    result = AgGrid(
        df,
        gridOptions=gridOptions,
        height=400,
        theme='streamlit',
        key='aggrid_return_demo'
    )

    # Display results
    col1, col2 = st.columns(2)

    with col1:
        st.markdown("**Grid Data:**")
        if result.data is not None:
            st.info(f"Total rows: {len(result.data)}")
        else:
            st.info("No data")

    with col2:
        st.markdown("**Selected Data:**")
        if result.selected_data is not None:
            st.success(f"Selected rows: {len(result.selected_data)}")
        else:
            st.info("No rows selected")

    # Show selected data
    if result.selected_data is not None and len(result.selected_data) > 0:
        with st.expander("View selected data"):
            st.dataframe(result.selected_data)

    # Show event data
    if result.event_data:
        with st.expander("View last event"):
            st.json(result.event_data)

    with st.expander("Show code", expanded=False):
        st.code("""
from streamlit_aggrid import AgGrid, GridOptionsBuilder
import streamlit as st
import pandas as pd

# Create sample data
df = pd.DataFrame({
    'athlete': ['Michael Phelps', 'Natalie Coughlin', 'Aleksey Nemov'],
    'age': [23, 25, 28],
    'country': ['United States', 'United States', 'Russia'],
    'sport': ['Swimming', 'Swimming', 'Gymnastics'],
    'gold': [8, 2, 4],
})

# Configure grid
gb = GridOptionsBuilder.from_dataframe(df)
gb.configure_default_column(resizable=True, filterable=True)
gb.configure_selection('multiple', use_checkbox=True)
gridOptions = gb.build()

# Render and get result
result = AgGrid(df, gridOptions=gridOptions)

# Access data
all_data = result.data                # All grid data
selected = result.selected_data       # Selected rows only
state = result.grid_state             # Grid state (filters, sorting, etc)
event = result.event_data             # Last user interaction

# Display results
if result.selected_data is not None:
    st.write(f"Selected {len(result.selected_data)} rows")
    st.dataframe(result.selected_data)
""", language="python")

    st.divider()


def section_api_header():
    """API Header"""
    st.title("AgGridReturn API", anchor='aggridreturn-api')


def section_data():
    """data property API"""
    st.header("data", anchor="data")

    st.code("""
@property
data -> pd.DataFrame | None
""", language="python")

    st.markdown("""
    Returns all grid data based on the `data_return_mode` setting.

    **Behavior by mode:**
    - `AS_INPUT` - All rows as originally provided
    - `FILTERED` - Only rows matching current filters
    - `FILTERED_AND_SORTED` - Filtered rows in current sort order

    **Returns:**
    - pd.DataFrame: Grid data, or None if empty

    **Example:**
    ```python
    from streamlit_aggrid.shared import DataReturnMode

    result = AgGrid(df, data_return_mode=DataReturnMode.FILTERED)

    # Get data respecting current filters
    current_data = result.data
    if current_data is not None:
        st.write(f"Showing {len(current_data)} rows")
    ```
    """)


def section_selected_data():
    """selected_data property API"""
    st.header("selected_data", anchor="selected-data")

    st.code("""
@property
selected_data -> pd.DataFrame | None
""", language="python")

    st.markdown("""
    Returns only the selected rows from the grid.

    **Returns:**
    - pd.DataFrame: Selected rows, or None if no selection

    **Note:** `selected_rows` is an alias for backward compatibility.

    **Example:**
    ```python
    result = AgGrid(df, gridOptions=gridOptions)

    if result.selected_data is not None:
        st.success(f"User selected {len(result.selected_data)} rows")

        # Process selected data
        for idx, row in result.selected_data.iterrows():
            process_row(row)
    else:
        st.info("No rows selected")
    ```
    """)


def section_dataGroups():
    """dataGroups property API"""
    st.header("dataGroups", anchor="datagroups")

    st.code("""
@property
dataGroups -> Dict[tuple, pd.DataFrame]
""", language="python")

    st.markdown("""
    Returns grouped data as a dictionary where keys are tuples of group values.

    This property is useful when working with row grouping (AG Grid Enterprise feature).
    Each key represents a group path, and the value is a DataFrame containing rows in that group.

    **Returns:**
    - Dict[tuple, pd.DataFrame]: Grouped data where:
        - Keys are tuples like `('Swimming',)` or `('Swimming', 'Michael Phelps')`
        - Values are DataFrames containing rows in that group

    **Related property:**
    - `selected_dataGroups` - Same structure but only for selected groups

    **Example:**
    ```python
    result = AgGrid(df, gridOptions=gridOptions, enable_enterprise_modules=True)

    # Access all groups
    for group_key, group_df in result.dataGroups.items():
        st.write(f"Group {group_key}: {len(group_df)} rows")

    # Access specific group
    swimming_data = result.dataGroups.get(('Swimming',))
    if swimming_data is not None:
        st.dataframe(swimming_data)

    # Filter by group level
    top_level = {k: v for k, v in result.dataGroups.items() if len(k) == 1}
    ```

    **Note:** Requires row grouping to be configured in gridOptions. Returns all data as `{(): DataFrame}` if no grouping is active.
    """)


def section_grid_state():
    """grid_state property API"""
    st.header("grid_state", anchor="grid-state")

    st.code("""
@property
grid_state -> Dict[str, Any] | None
""", language="python")

    st.markdown("""
    Returns the complete grid state including filters, sorting, column order, and row selection.

    This state can be saved and restored later using AG Grid's `initialState` option.

    **Returns:**
    - Dict: Grid state object containing:
        - `filter` - Active filters
        - `sort` - Sort configuration
        - `columnOrder` - Column positions
        - `rowSelection` - Selected row IDs
        - `pagination` - Current page
        - And more...

    **Related properties:**
    - `selected_rows_id` - Just the selected row IDs
    - `columns_state` - Column-specific state

    **Example:**
    ```python
    # Save grid state to session
    result = AgGrid(df, gridOptions=gridOptions, key='my_grid')

    if result.grid_state:
        st.session_state['saved_state'] = result.grid_state

    # Restore grid state later
    if 'saved_state' in st.session_state:
        gb = GridOptionsBuilder.from_dataframe(df)
        gb.configure_grid_options(
            initialState=st.session_state['saved_state']
        )
        gridOptions = gb.build()
        result = AgGrid(df, gridOptions=gridOptions)
    ```

    See [AG Grid State Documentation](https://ag-grid.com/javascript-data-grid/grid-state/) for details.
    """)


def section_columns_state():
    """columns_state property API"""
    st.header("columns_state", anchor="columns-state")

    st.code("""
@property
columns_state -> Dict[str, Any] | None
""", language="python")

    st.markdown("""
    Returns the state of columns including visibility, width, order, and pinning.

    **Returns:**
    - Dict: Column state information for each column

    **Example:**
    ```python
    result = AgGrid(df, gridOptions=gridOptions)

    if result.columns_state:
        # Save column widths
        widths = {
            col['colId']: col.get('width')
            for col in result.columns_state
        }

        # Check which columns are hidden
        hidden = [
            col['colId']
            for col in result.columns_state
            if col.get('hide', False)
        ]

        st.write(f"Hidden columns: {hidden}")
    ```
    """)


def section_event_data():
    """event_data property API"""
    st.header("event_data", anchor="event-data")

    st.code("""
@property
event_data -> Dict[str, Any]
""", language="python")

    st.markdown("""
    Returns information about the last event that triggered the grid update.

    **Returns:**
    - Dict: Event data containing:
        - `type` - Event type (e.g., 'selectionChanged', 'cellValueChanged')
        - Additional event-specific data

    **Example:**
    ```python
    result = AgGrid(df, gridOptions=gridOptions)

    if result.event_data:
        event_type = result.event_data.get('type')

        if event_type == 'cellValueChanged':
            st.info("A cell was edited")
            # Handle cell edit

        elif event_type == 'selectionChanged':
            st.info("Selection changed")
            # Handle selection change
    ```

    **Common event types:**
    - `selectionChanged` - Row selection changed
    - `cellValueChanged` - Cell was edited
    - `filterChanged` - Filter was applied/removed
    - `sortChanged` - Sort order changed
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

if SECTIONS.get('data', False):
    section_data()

if SECTIONS.get('selected_data', False):
    section_selected_data()

if SECTIONS.get('dataGroups', False):
    section_dataGroups()

if SECTIONS.get('grid_state', False):
    section_grid_state()

if SECTIONS.get('columns_state', False):
    section_columns_state()

if SECTIONS.get('event_data', False):
    section_event_data()


# ============================================================================
# FOOTER
# ============================================================================

st.divider()

st.info("""
**Learn More:**

- [AG Grid State Management](https://ag-grid.com/javascript-data-grid/grid-state/)
- [AG Grid Events](https://ag-grid.com/javascript-data-grid/grid-events/)
- [AG Grid Row Selection](https://ag-grid.com/javascript-data-grid/row-selection/)

Check out other documentation pages for detailed examples on filtering, editing, and row grouping.
""")