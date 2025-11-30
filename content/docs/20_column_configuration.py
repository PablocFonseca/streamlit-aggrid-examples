"""
Column Configuration & Customization
=====================================

This guide demonstrates how to configure and customize columns in AgGrid.
Inspired by AG Grid documentation on column configuration, headers, groups, sizing, moving, and pinning.
"""

import streamlit as st
from st_aggrid import AgGrid, GridOptionsBuilder
from pathlib import Path
import pandas as pd

st.set_page_config(page_title="Column Configuration", layout="wide")

# ============================================================================
# SECTION CONTROL - Set to True/False to enable/disable sections
# ============================================================================
SECTIONS = {
    'overview': True,
    'column_headers': True,
    'value_formatters': True,
    'column_sizing': True,
    'column_pinning': True,
    'column_moving': True,
    'column_groups': True,
    'complete_example': True,
}

# Load Olympic data
data_path = Path(__file__).parent.parent.parent.joinpath(
    "assets", "olympic-winners.json"
)


@st.cache_data
def load_olympic_data():
    """Load Olympic winners data as a DataFrame for use in examples."""
    return pd.read_json(data_path)


# Sidebar navigation/index
with st.sidebar:
    st.markdown('''
    <div class="sidebar-nav-section">On this page</div>
    <div class="sidebar-nav-container">
        <a href="#overview" class="sidebar-nav-link">Overview</a>
        <a href="#column-headers" class="sidebar-nav-link">Column Headers</a>
        <a href="#value-formatters" class="sidebar-nav-link">Value Formatters</a>
        <a href="#column-sizing" class="sidebar-nav-link">Column Sizing</a>
        <a href="#column-pinning" class="sidebar-nav-link">Column Pinning</a>
        <a href="#column-moving" class="sidebar-nav-link">Column Moving</a>
        <a href="#column-groups" class="sidebar-nav-link">Column Groups</a>
        <a href="#complete-example" class="sidebar-nav-link">Complete Example</a>
    </div>
    ''', unsafe_allow_html=True)

st.title("Column Configuration & Customization")

st.markdown("""
This guide demonstrates the various ways to configure and customize columns in AgGrid,
from basic header customization to advanced features like pinning and grouping.
""")

df = load_olympic_data()


# ============================================================================
# SECTION FUNCTIONS
# ============================================================================

def section_overview():
    """Overview Section"""
    st.header("Overview", anchor="overview")

    st.markdown("""
    AG Grid offers extensive column configuration options. You can customize:
    - **Headers**: Names, styling, tooltips
    - **Formatting**: How values are displayed using valueFormatters
    - **Sizing**: Width, flex, min/max constraints
    - **Positioning**: Pinning, moving, ordering
    - **Grouping**: Organize related columns under parent headers
    """)


def section_column_headers():
    """Column Headers Section"""
    st.header("Column Headers", anchor="column-headers")

    st.markdown("""
    Customize column headers to make your grid more readable and professional.
    You can set custom names, apply styles, and configure header properties.
    """)

    with st.expander("Show code", expanded=False):
        st.code(
            """
from st_aggrid import AgGrid, GridOptionsBuilder

# Create builder from dataframe
gb = GridOptionsBuilder.from_dataframe(data)

# Configure custom header names
gb.configure_column('athlete', header_name='Athlete Name')
gb.configure_column('country', header_name='Country/Region')
gb.configure_column('total', header_name='Total Medals')

# Apply header styling
gb.configure_column('gold',
    header_name='🥇 Gold',
    headerClass='gold-header'
)

gb.configure_column('silver',
    header_name='🥈 Silver',
    headerClass='silver-header'
)

gb.configure_column('bronze',
    header_name='🥉 Bronze',
    headerClass='bronze-header'
)

gridOptions = gb.build()
AgGrid(data_path, gridOptions=gridOptions)
""",
            language="python",
        )

    st.markdown("**Output:**")
    st.info("Notice the custom header names and medal emoji in the column headers.")

    gb_headers = GridOptionsBuilder.from_dataframe(df)

    gb_headers.configure_column("athlete", header_name="Athlete Name", minWidth=150)
    gb_headers.configure_column("country", header_name="Country/Region")
    gb_headers.configure_column("total", header_name="Total Medals")
    gb_headers.configure_column("gold", header_name="🥇 Gold")
    gb_headers.configure_column("silver", header_name="🥈 Silver")
    gb_headers.configure_column("bronze", header_name="🥉 Bronze")

    gridOptions_headers = gb_headers.build()
    AgGrid(data_path, gridOptions=gridOptions_headers, height=300, key="headers_example")


def section_value_formatters():
    """Value Formatters Section"""
    st.header("Value Formatters", anchor="value-formatters")

    st.markdown("""
    [Value Formatters](https://ag-grid.com/react-data-grid/value-formatters/) control how data is displayed without changing the underlying values.
    Use JavaScript expressions to format numbers, dates, and strings.
    """)

    with st.expander("Show code", expanded=False):
        st.code(
            """
gb = GridOptionsBuilder.from_dataframe(data)

# Format numbers with locale formatting
gb.configure_column('gold',
    valueFormatter="value.toLocaleString()"
)

# Format dates from DD/MM/YYYY string to readable format
gb.configure_column('date',
    valueFormatter="new Date(value).toLocaleString('en-US', {  weekday: 'long',  year: 'numeric',  month: 'long',  day: 'numeric'})"
)

# Conditional formatting: Add trophy emoji for high medal counts
gb.configure_column('total',
    header_name='Total Medals',
    valueFormatter="value >= 5 ? '🏆 ' + value : value"
)

# String manipulation: Uppercase country codes
gb.configure_column('sport',
    valueFormatter="value.toUpperCase()"
)

# Number formatting with fixed decimals (if we had decimal values)
# gb.configure_column('score',
#     valueFormatter="value.toFixed(2)"
# )

gridOptions = gb.build()
AgGrid(data_path, gridOptions=gridOptions)
""",
            language="python",
        )

    st.markdown("**Output:**")
    st.info("""
    Formatting applied:
    - Date uses custom formatting
    - Total medals show 🏆 trophy when count >= 5
    - Sports are displayed in UPPERCASE
    """)

    gb_formatters = GridOptionsBuilder.from_dataframe(df)

    gb_formatters.configure_default_column(minWidth=50)
    gb_formatters.configure_column("athlete", minWidth=150)
    gb_formatters.configure_column(
        "date",
        valueFormatter="""new Date(value).toLocaleString('en-US', {  weekday: "long",  year: "numeric",  month: "long",  day: "numeric",})""",
        minWidth=200,
    )
    gb_formatters.configure_column(
        "gold", header_name="🥇 Gold", valueFormatter="value.toLocaleString()"
    )
    gb_formatters.configure_column(
        "total",
        header_name="Total Medals",
        valueFormatter="value >= 5 ? '🏆 ' + value : value",
    )
    gb_formatters.configure_column("sport", valueFormatter="value.toUpperCase()")

    gridOptions_formatters = gb_formatters.build()
    AgGrid(
        data_path, gridOptions=gridOptions_formatters, height=300, key="formatters_example"
    )


def section_column_sizing():
    """Column Sizing Section"""
    st.header("Column Sizing", anchor="column-sizing")

    st.markdown("""
    Control column widths using various sizing strategies:
    - **Fixed width**: Specific pixel width
    - **Flex**: Proportional distribution of available space
    - **Min/Max**: Constraints on resizable columns
    - **Resizable**: Allow users to resize columns
    - **Group resizing**: When resizing column groups, extra space is distributed among resizable columns within the group
    """)

    with st.expander("Show code", expanded=False):
        st.code(
            """
gb = GridOptionsBuilder.from_dataframe(data)

# Make all columns resizable by default
gb.configure_default_column(resizable=True)

# Configure individual columns
gb.configure_column('athlete', header_name='Athlete', minWidth=120, flex=2)
gb.configure_column('age', flex=1, minWidth=80)
gb.configure_column('country', minWidth=100, flex=1)

# Create Athlete Info group
gb.configure_column(
    header_name='Athlete Info',
    children=['athlete', 'age', 'country']
)

# Medal columns with fixed widths
gb.configure_column('gold', header_name='🥇 Gold', width=100)
gb.configure_column('silver', header_name='🥈 Silver', width=100)
gb.configure_column('bronze', header_name='🥉 Bronze', width=100)
gb.configure_column('total', header_name='Total', width=100)

# Create Medal Counts group (resizable group)
gb.configure_column(
    header_name='Medal Counts',
    children=['gold', 'silver', 'bronze', 'total']
)

# Other columns
gb.configure_column('year', minWidth=80, maxWidth=120)
gb.configure_column('sport', flex=1)
gb.configure_column('date', width=120, resizable=False)

gridOptions = gb.build()
AgGrid(data_path, gridOptions=gridOptions)
""",
            language="python",
        )

    st.markdown("**Output:**")
    st.info("""
    Try resizing columns and groups by dragging their edges:
    - **Age** has minimum 80px width and flex size of 1
    - **Athlete Info group**: Resize the group header to distribute space among resizable children (athlete, country)
    - **Medal Counts group**: Resize the group header to distribute space equally among all medal columns
    - **Athlete** and **Country** use flex sizing of 2
    - **Year** is constrained between 80-120px
      **Date** is fixed to 120px and cannot be resized
    """)

    gb_sizing = GridOptionsBuilder.from_dataframe(df)

    gb_sizing.configure_default_column(resizable=True)

    # Athlete Info group
    gb_sizing.configure_column("athlete", header_name="Athlete", minWidth=120, flex=2)
    gb_sizing.configure_column("age", flex=1, minWidth=80)
    gb_sizing.configure_column("country", minWidth=100, flex=2)

    gb_sizing.configure_column(
        header_name="Athlete Info", children=["athlete", "age", "country"]
    )

    # Medal Counts group
    gb_sizing.configure_column("gold", header_name="🥇 Gold", width=100)
    gb_sizing.configure_column("silver", header_name="🥈 Silver", width=100)
    gb_sizing.configure_column("bronze", header_name="🥉 Bronze", width=100)
    gb_sizing.configure_column("total", header_name="Total", width=100)

    gb_sizing.configure_column(
        header_name="Medal Counts", children=["gold", "silver", "bronze", "total"]
    )

    # Other columns
    gb_sizing.configure_column("year", minWidth=80, maxWidth=120)
    gb_sizing.configure_column("sport", flex=1)
    gb_sizing.configure_column("date", width=120, resizable=False)

    gridOptions_sizing = gb_sizing.build()
    AgGrid(data_path, gridOptions=gridOptions_sizing, height=300, key="sizing_example")


def section_column_pinning():
    """Column Pinning Section"""
    st.header("Column Pinning", anchor="column-pinning")

    st.markdown("""
    Pin columns to the left or right side of the grid so they remain visible during horizontal scrolling.
    This is useful for keeping key identifier columns (like names) or summary columns (like totals) always visible.
    """)

    with st.expander("Show code", expanded=False):
        st.code(
            """
gb = GridOptionsBuilder.from_dataframe(data)

# Pin athlete name to the left (always visible)
gb.configure_column('athlete',
    header_name='Athlete Name',
    pinned='left',
    minWidth=150
)

# Pin total medals to the right
gb.configure_column('total',
    header_name='Total',
    pinned='right',
    width=100
)

# Configure other columns normally
gb.configure_default_column(minWidth=100)

gridOptions = gb.build()
AgGrid(data_path, gridOptions=gridOptions)
""",
            language="python",
        )

    st.markdown("**Output:**")
    st.info("""
    The athlete name is pinned to the left and total medals to the right.
    Scroll horizontally to see how these columns stay in place while others scroll.
    """)

    gb_pinning = GridOptionsBuilder.from_dataframe(df)

    gb_pinning.configure_column(
        "athlete", header_name="Athlete Name", pinned="left", minWidth=300
    )
    gb_pinning.configure_column("total", header_name="Total", pinned="right", width=300)
    gb_pinning.configure_default_column(minWidth=100)

    gridOptions_pinning = gb_pinning.build()
    AgGrid(data_path, gridOptions=gridOptions_pinning, height=300, key="pinning_example")


def section_column_moving():
    """Column Moving Section"""
    st.header("Column Moving", anchor="column-moving")

    st.markdown("""
    By default, users can reorder columns by dragging them. You can disable this for specific columns
    or for the entire grid using the `suppressMovable` property.
    """)

    with st.expander("Show code", expanded=False):
        st.code(
            """
gb = GridOptionsBuilder.from_dataframe(data)

# Lock the athlete column in place (cannot be moved)
gb.configure_column('athlete',
    header_name='Athlete Name',
    suppressMovable=True,
    pinned='left'
)

# Lock total medals column
gb.configure_column('total',
    suppressMovable=True,
    pinned='right'
)

# All other columns can be freely moved
gb.configure_default_column(minWidth=100)

gridOptions = gb.build()
AgGrid(data_path, gridOptions=gridOptions)
""",
            language="python",
        )

    st.markdown("**Output:**")
    st.info("""
    Try dragging column headers to reorder them:
    - Athlete Name and sport columns are locked and cannot be moved
    - All other columns can be freely reordered by dragging
    """)

    gb_moving = GridOptionsBuilder.from_dataframe(df)

    gb_moving.configure_column(
        "athlete",
        header_name="Athlete Name",
        suppressMovable=True,
        pinned="left",
        minWidth=150,
    )
    gb_moving.configure_column("sport", suppressMovable=True, width=100)
    gb_moving.configure_default_column(minWidth=100)

    gridOptions_moving = gb_moving.build()
    AgGrid(data_path, gridOptions=gridOptions_moving, height=300, key="moving_example")


def section_column_groups():
    """Column Groups Section"""
    st.header("Column Groups", anchor="column-groups")

    st.markdown("""
    Column groups organize related columns under a parent header. This provides better visual organization
    for complex grids with many columns.

    You can now create column groups using GridOptionsBuilder by passing the `children` parameter to `configure_column()`.
    """)

    with st.expander("Show code", expanded=False):
        st.code(
            """
from st_aggrid import AgGrid, GridOptionsBuilder

gb = GridOptionsBuilder.from_dataframe(data)

# Configure individual columns first
gb.configure_column('athlete', header_name='Name', minWidth=150)
gb.configure_column('age', width=80)
gb.configure_column('country', minWidth=120)

gb.configure_column('year', width=100)
gb.configure_column('date', width=120)
gb.configure_column('sport', minWidth=120)

gb.configure_column('gold', header_name='🥇 Gold', width=100)
gb.configure_column('silver', header_name='🥈 Silver', width=100)
gb.configure_column('bronze', header_name='🥉 Bronze', width=100)
gb.configure_column('total', header_name='Total', width=100,
    valueFormatter="value >= 5 ? '🏆 ' + value : value")

# Now create the groups by specifying children
gb.configure_column(
    header_name='Athlete Info',
    children=['athlete', 'age', 'country']
)

gb.configure_column(
    header_name='Event Details',
    children=['year', 'date', 'sport']
)

gb.configure_column(
    header_name='Medal Counts',
    children=['gold', 'silver', 'bronze', 'total']
)

# Set default properties
gb.configure_default_column(resizable=True, sortable=True, filter=True)

gridOptions = gb.build()
AgGrid(data_path, gridOptions=gridOptions)
""",
            language="python",
        )

    st.markdown("**Output:**")
    st.info("""
    Columns are organized into three groups:
    - **Athlete Info**: Name, age, country
    - **Event Details**: Year, date, sport
    - **Medal Counts**: Gold, silver, bronze, total

    Notice how we configure individual columns first, then group them using the same `configure_column()` method!
    """)

    gb_groups = GridOptionsBuilder.from_dataframe(df)

    # Configure individual columns
    gb_groups.configure_column("athlete", header_name="Name", minWidth=150)
    gb_groups.configure_column("age", width=80)
    gb_groups.configure_column("country", minWidth=120)
    gb_groups.configure_column("year", width=100)
    gb_groups.configure_column("date", width=120)
    gb_groups.configure_column("sport", minWidth=120)
    gb_groups.configure_column("gold", header_name="🥇 Gold", width=100)
    gb_groups.configure_column("silver", header_name="🥈 Silver", width=100)
    gb_groups.configure_column("bronze", header_name="🥉 Bronze", width=100)
    gb_groups.configure_column(
        "total",
        header_name="Total",
        width=100,
        valueFormatter="value >= 5 ? '🏆 ' + value : value",
    )

    # Create groups
    gb_groups.configure_column(
        header_name="Athlete Info", children=["athlete", "age", "country"]
    )
    gb_groups.configure_column(
        header_name="Event Details", children=["year", "date", "sport"]
    )
    gb_groups.configure_column(
        header_name="Medal Counts", children=["gold", "silver", "bronze", "total"]
    )

    gb_groups.configure_default_column(resizable=True, sortable=True, filter=True)

    gridOptions_groups = gb_groups.build()
    AgGrid(data_path, gridOptions=gridOptions_groups, height=300, key="groups_example")


def section_complete_example():
    """Complete Example Section"""
    st.header("Complete Example", anchor="complete-example")

    st.markdown("""
    Here's a comprehensive example combining all column configuration features:
    - Column groups for organization
    - Custom headers with emoji
    - Value formatters for numbers and conditionals
    - Pinned columns for key data
    - Mixed sizing strategies
    - Locked columns to prevent moving
    """)

    with st.expander("Show code", expanded=False):
        st.code(
            """
from st_aggrid import AgGrid, GridOptionsBuilder

gb = GridOptionsBuilder.from_dataframe(data)

# Configure default column properties
gb.configure_default_column(resizable=True, sortable=True, filter=True)

# Athlete Info group
gb.configure_column('athlete',
    header_name='🏃 Athlete Name',
    pinned='left',
    suppressMovable=True,
    minWidth=180,
    flex=2
)
gb.configure_column('age', header_name='Age', width=80, type=['numericColumn'])
gb.configure_column('country', header_name='Country/Region', minWidth=140, flex=1)

gb.configure_column(
    header_name='Athlete Info',
    children=['athlete', 'age', 'country']
)

# Event Details group
gb.configure_column('year', header_name='Year', width=100)
gb.configure_column('date', header_name='Date', width=130)
gb.configure_column('sport',
    header_name='Sport',
    minWidth=140,
    valueFormatter='value.toUpperCase()'
)

gb.configure_column(
    header_name='Event Details',
    children=['year', 'date', 'sport']
)

# Medal Counts group
gb.configure_column('gold',
    header_name='🥇 Gold',
    width=100,
    type=['numericColumn'],
    valueFormatter='value.toLocaleString()'
)
gb.configure_column('silver',
    header_name='🥈 Silver',
    width=100,
    type=['numericColumn'],
    valueFormatter='value.toLocaleString()'
)
gb.configure_column('bronze',
    header_name='🥉 Bronze',
    width=100,
    type=['numericColumn'],
    valueFormatter='value.toLocaleString()'
)
gb.configure_column('total',
    header_name='Total',
    width=110,
    pinned='right',
    suppressMovable=True,
    type=['numericColumn'],
    valueFormatter="value >= 5 ? '🏆 ' + value : value",
    cellStyle={'fontWeight': 'bold'}
)

gb.configure_column(
    header_name='🏅 Medal Counts',
    children=['gold', 'silver', 'bronze', 'total']
)

gridOptions = gb.build()
AgGrid(data_path, gridOptions=gridOptions, height=400)
""",
            language="python",
        )

    st.markdown("**Output:**")
    st.info("""
    This grid combines all features demonstrated:
    - Three column groups with clear headers
    - Athlete name pinned left, Total pinned right
    - Custom emoji in headers
    - Sports in UPPERCASE
    - Trophy icon for 5+ total medals
    - Flexible sizing with constraints
    - All columns resizable, sortable, and filterable
    """)

    gb_complete = GridOptionsBuilder.from_dataframe(df)

    # Configure default column properties
    gb_complete.configure_default_column(resizable=True, sortable=True, filter=True)

    # Athlete Info group
    gb_complete.configure_column(
        "athlete",
        header_name="🏃 Athlete Name",
        pinned="left",
        suppressMovable=True,
        minWidth=180,
        flex=2,
    )
    gb_complete.configure_column("age", header_name="Age", width=80, type=["numericColumn"])
    gb_complete.configure_column(
        "country", header_name="Country/Region", minWidth=140, flex=1
    )

    gb_complete.configure_column(
        header_name="Athlete Info", children=["athlete", "age", "country"]
    )

    # Event Details group
    gb_complete.configure_column("year", header_name="Year", width=100)
    gb_complete.configure_column("date", header_name="Date", width=130)
    gb_complete.configure_column(
        "sport", header_name="Sport", minWidth=140, valueFormatter="value.toUpperCase()"
    )

    gb_complete.configure_column(
        header_name="Event Details", children=["year", "date", "sport"]
    )

    # Medal Counts group
    gb_complete.configure_column(
        "gold",
        header_name="🥇 Gold",
        width=100,
        type=["numericColumn"],
        valueFormatter="value.toLocaleString()",
    )
    gb_complete.configure_column(
        "silver",
        header_name="🥈 Silver",
        width=100,
        type=["numericColumn"],
        valueFormatter="value.toLocaleString()",
    )
    gb_complete.configure_column(
        "bronze",
        header_name="🥉 Bronze",
        width=100,
        type=["numericColumn"],
        valueFormatter="value.toLocaleString()",
    )
    gb_complete.configure_column(
        "total",
        header_name="Total",
        width=110,
        pinned="right",
        suppressMovable=True,
        type=["numericColumn"],
        valueFormatter="value >= 5 ? '🏆 ' + value : value",
        cellStyle={"fontWeight": "bold"},
    )

    gb_complete.configure_column(
        header_name="🏅 Medal Counts", children=["gold", "silver", "bronze", "total"]
    )

    gridOptions_complete = gb_complete.build()
    AgGrid(data_path, gridOptions=gridOptions_complete, height=400, key="complete_example")


# ============================================================================
# RENDER SECTIONS BASED ON CONFIGURATION
# ============================================================================

if SECTIONS.get('overview', False):
    section_overview()

if SECTIONS.get('column_headers', False):
    section_column_headers()

if SECTIONS.get('value_formatters', False):
    section_value_formatters()

if SECTIONS.get('column_sizing', False):
    section_column_sizing()

if SECTIONS.get('column_pinning', False):
    section_column_pinning()

if SECTIONS.get('column_moving', False):
    section_column_moving()

if SECTIONS.get('column_groups', False):
    section_column_groups()

if SECTIONS.get('complete_example', False):
    section_complete_example()


# ============================================================================
# FOOTER
# ============================================================================

st.divider()

st.info("""
**Learn More:**

For more advanced column configuration options:

- [AG Grid Column Properties](https://www.ag-grid.com/javascript-data-grid/column-properties/)
- [AG Grid Column Headers](https://www.ag-grid.com/javascript-data-grid/column-headers/)
- [AG Grid Column Groups](https://www.ag-grid.com/javascript-data-grid/column-groups/)
- [AG Grid Column Sizing](https://www.ag-grid.com/javascript-data-grid/column-sizing/)
- [AG Grid Column Pinning](https://www.ag-grid.com/javascript-data-grid/column-pinning/)

Check out other documentation pages for more examples and use cases.
""")
