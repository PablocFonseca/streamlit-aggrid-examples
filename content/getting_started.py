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

st.title("Getting Started")

st.markdown(
    """
Installation
------------

Install streamlit-aggrid using pip:

```bash
pip install streamlit-aggrid
```

Basic Usage
-----------

The simplest way to use AgGrid is to pass a pandas DataFrame as the only argument.
The grid will automatically infer column names, data types, and apply appropriate
formatting (e.g., right-aligned numbers, formatted dates).
"""
)

st.subheader("Example 1: DataFrame Input")

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
    {"Name": ["Alice", "Bob", "Charlie"], "Age": [25, 30, 35], "Score": [92.5, 87.3, 95.1]}
)

AgGrid(df, key="example1")

st.markdown(
    """
Using JSON Data
---------------

You can work with JSON data either from external files or in-memory as Python lists of dictionaries.
"""
)

st.subheader("Example 2: JSON Data")

st.code(
    """
from st_aggrid import AgGrid

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


json_data = Path(__file__).parent.parent.joinpath("assets","olympic-winners.json")
AgGrid(json_data, height=300, key="example2")
