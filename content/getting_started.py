"""
Getting Started
===============

This guide will help you get started with streamlit-aggrid and demonstrate basic usage patterns.
"""

from pathlib import Path
import streamlit as st
from st_aggrid import AgGrid
import pandas as pd

st.set_page_config(page_title="Getting Started", layout="centered")

# Sidebar navigation/index
with st.sidebar:
    st.title("Getting Started")
    st.markdown("""
    - [Installation](#installation)
    - [Basic Usage](#basic-usage)
    - [DataFrame Input](#dataframe-input)
    - [JSON Data](#json-data)
    - [Custom Grid Options](#custom-grid-options)
    - [Learn More](#learn-more)
    """)

st.title("Getting Started")

st.markdown("This guide will help you get started with streamlit-aggrid and demonstrate basic usage patterns.")

# Installation Section
st.header("Installation", anchor="installation")

st.markdown("Install streamlit-aggrid using pip:")

st.code("pip install streamlit-aggrid", language="bash")

# Basic Usage Section
st.header("Basic Usage", anchor="basic-usage")

st.markdown("""
The simplest way to use AgGrid is to pass a pandas (or polars) DataFrame as the only argument.
The grid will automatically infer column names, data types, and apply appropriate
formatting (e.g., right-aligned numbers, formatted dates).
""")

# Example 1: DataFrame Input
st.subheader("DataFrame Input", anchor="dataframe-input")

with st.expander("Show code", expanded=False):
    st.code(
        """
import streamlit as st
from st_aggrid import AgGrid
import pandas as pd

df = pd.DataFrame({
    'Name': ['Alice', 'Bob', 'Charlie'],
    'Age': [25, 30, 35],
    'Score': [92.5, 87.3, 95.1]
})

AgGrid(df)
""",
        language="python",
    )

df = pd.DataFrame(
    {
        "Name": ["Alice", "Bob", "Charlie"],
        "Age": [25, 30, 35],
        "Score": [92.5, 87.3, 95.1],
    }
)

AgGrid(df, key="example1", height=200)

# Example 2: JSON Data
st.subheader("JSON Data", anchor="json-data")

st.markdown("""
You can work with JSON data either from external files or in-memory as Python lists of dictionaries.
""")

with st.expander("Show code", expanded=False):
    st.code(
        """
from st_aggrid import AgGrid
from pathlib import Path

# In-memory JSON data
data = '''[
    {
        "athlete": "Michael Phelps",
        "age": 23,
        "country": "United States",
        "year": 2008,
        "sport": "Swimming",
        "gold": 8,
        "silver": 0,
        "bronze": 0
    },
    {
        "athlete": "Usain Bolt",
        "age": 22,
        "country": "Jamaica",
        "year": 2008,
        "sport": "Athletics",
        "gold": 3,
        "silver": 0,
        "bronze": 0
    },
    {
        "athlete": "Simone Biles",
        "age": 19,
        "country": "United States",
        "year": 2016,
        "sport": "Gymnastics",
        "gold": 4,
        "silver": 0,
        "bronze": 1
    }
]'''

AgGrid(data)

# Or load from an external JSON file
AgGrid("./olympic-winners.json")
""",
        language="python",
    )

json_data = Path(__file__).parent.parent.joinpath("assets", "olympic-winners.json")
AgGrid(json_data, height=300, key="example2")

# Example 3: Custom Grid Options
st.subheader("Custom Grid Options", anchor="custom-grid-options")

st.markdown("""
For advanced customization, you can pass `gridOptions` to configure the grid behavior and appearance.
AG Grid offers extensive customization options through its configuration API.

**Enterprise Features:** If you hold a valid AG Grid Enterprise license, you can enable enterprise
features by setting `enable_enterprise_modules=True` to access advanced functionality like
row grouping, pivoting, aggregation, and more.
""")

st.info("""
**Try it out:**
- **Double-click any cell** to edit values
- **Click the sidebar icon** (top right) to access columns and filters panels
- **Check the status bar** (bottom) showing row counts
- **Notice the striped rows** with alternating background colors for better readability
- **See custom header names** that differ from the actual column names (e.g., "Full Name" instead of "Name")
""")

with st.expander("Show code", expanded=False):
    st.code(
        """
from st_aggrid import AgGrid
import pandas as pd

df = pd.DataFrame({
    'Name': ['Alice', 'Bob', 'Charlie', 'David', 'Eve'],
    'Age': [25, 30, 35, 28, 42],
    'Score': [92.5, 87.3, 95.1, 88.0, 91.2],
    'Grade': ['A', 'B', 'A', 'B', 'A']
})

gridOptions = {
    'columnDefs': [
        {'field': 'Name', 'headerName': 'Full Name'},
        {'field': 'Age', 'headerName': 'Age', 'type': 'numericColumn'},
        {'field': 'Score', 'headerName': 'Test Score', 'type': 'numericColumn',
         'valueFormatter': 'value.toFixed(1)'},
        {'field': 'Grade', 'headerName': 'Letter Grade'},
    ],
    'defaultColDef': {
        'editable': True,
        'sortable': True,
        'filter': True,
        'resizable': True,
    },
    'statusBar': {
        'statusPanels': [
            {'statusPanel': 'agTotalRowCountComponent', 'align': 'left'},
            {'statusPanel': 'agFilteredRowCountComponent'},
            {'statusPanel': 'agSelectedRowCountComponent'},
            {'statusPanel': 'agAggregationComponent'}
        ]
    },
    'sideBar': {
        'toolPanels': ['columns', 'filters']
    },
    'rowClassRules': {
        'even-row': 'node.rowIndex % 2 === 0',
        'odd-row': 'node.rowIndex % 2 !== 0'
    }
}

custom_css = \"\"\"
    .even-row {
        background-color: var(--st-background-color);
    }
    .odd-row {
        background-color: var(--st-secondary-background-color);
    }
\"\"\"

st.write(f"<style>{custom_css}</style>", unsafe_allow_html=True)

AgGrid(df, gridOptions=gridOptions, custom_css=custom_css,
       isolate_styles=False, enable_enterprise_modules=True)
""",
        language="python",
    )

df_custom = pd.DataFrame(
    {
        "Name": ["Alice", "Bob", "Charlie", "David", "Eve"],
        "Age": [25, 30, 35, 28, 42],
        "Score": [92.5, 87.3, 95.1, 88.0, 91.2],
        "Grade": ["A", "B", "A", "B", "A"],
    }
)

gridOptions = {
    "columnDefs": [
        {"field": "Name", "headerName": "Full Name"},
        {"field": "Age", "headerName": "Age", "type": "numericColumn"},
        {
            "field": "Score",
            "headerName": "Test Score",
            "type": "numericColumn",
            "valueFormatter": "value.toFixed(1)",
        },
        {"field": "Grade", "headerName": "Letter Grade"},
    ],
    "defaultColDef": {
        "editable": True,
        "sortable": True,
        "filter": True,
        "resizable": True,
    },
    "statusBar": {
        "statusPanels": [
            {"statusPanel": "agTotalRowCountComponent", "align": "left"},
            {"statusPanel": "agFilteredRowCountComponent"},
            {"statusPanel": "agSelectedRowCountComponent"},
            {"statusPanel": "agAggregationComponent"},
        ]
    },
    "sideBar": {"toolPanels": ["columns", "filters"]},
    "rowClassRules": {
        "even-row": "node.rowIndex % 2 === 0",
        "odd-row": "node.rowIndex % 2 !== 0",
    },
}

custom_css = """
    .even-row {
        background-color: var(--st-background-color);
    }

    .odd-row {
        background-color: var(--st-secondary-background-color);
    }
"""
st.write(f"<style>{custom_css}</style>", unsafe_allow_html=True)

AgGrid(
    df_custom,
    gridOptions=gridOptions,
    key="example3",
    height=300,
    enable_enterprise_modules=True,
    isolate_styles=False
)

# Learn More Section
st.header("Learn More", anchor="learn-more")

st.markdown("""
AG Grid provides hundreds of configuration options for advanced features like custom cell renderers,
row grouping, pivoting, aggregation, and more. Check out the official AG Grid documentation
to explore all available options:

- [Grid Options Reference](https://www.ag-grid.com/javascript-data-grid/grid-options/)
- [Column Properties](https://www.ag-grid.com/javascript-data-grid/column-properties/)

For streamlit-aggrid specific examples and helpers, explore the **User Guide** and **Demos** sections
in this app.
""")