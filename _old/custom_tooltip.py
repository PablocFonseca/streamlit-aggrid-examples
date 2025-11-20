from st_aggrid import JsCode, AgGrid
import streamlit as st
import requests
import pandas as pd


st.title("Custom Tooltips")

st.markdown("""
This example demonstrates how to create a custom tooltip using the `tooltipComponent` property,
 as in the ag-grid website [example](https://www.ag-grid.com/javascript-data-grid/tooltips/#interactive-tooltips).
[Link to CodeSandbox](https://codesandbox.io/p/sandbox/hcvphv)  
    
  
  
The example below shows Tooltip Interaction with Custom Tooltips. Note the following:

- Tooltip is enabled for the Athlete and Age columns.  
- Tooltips will not disappear while being hovered.  
- The custom tooltip displays a text input and a Submit button which when clicked, 
updates the value of the Athlete Column cell in the hovered row and then closes itself by calling `hideTooltipCallback()`.
""")


CustomTooltip = JsCode("""
class CustomTooltip  {
    eGui;
    params;

    constructor() {
        this.onFormSubmit = this.onFormSubmit.bind(this);
    }

    init(params) {
        this.params = params;
        const type = params.type || 'primary';
        const data = params.api.getDisplayedRowAtIndex(params.rowIndex).data;
        const eGui = (this.eGui = document.createElement('div'));
        
        //hackish way to add css to the document. (https://stackoverflow.com/questions/524696/how-to-create-a-style-tag-with-javascript)
        const head = document.head;
        const css = `.custom-tooltip {
                        color: var(--ag-foreground-color);
                        background-color: #5577cc;
                        padding: 5px;
                    }

                    .custom-tooltip p,
                    .custom-tooltip h3 {
                        margin: 5px;
                        white-space: nowrap;
                    }

                    .custom-tooltip p:first-of-type {
                        font-weight: bold;
                    }`;

                       
        let style = document.createElement('style');
        style.type = 'text/css';
                       
        if (style.styleSheet){
        // This is required for IE8 and below.
        style.styleSheet.cssText = css;
        } else {
        style.appendChild(document.createTextNode(css));
        }
                       
        head.appendChild(style);
                            

        eGui.classList.add('custom-tooltip');
        eGui.innerHTML = `
            <div class="panel panel-${type}">
                <div class="panel-heading">
                    <h3 class="panel-title">${data.country}</h3>
                </div>
                <form class="panel-body">
                    <div class="form-group">
                        <input type="text" class="form-control" id="name" placeholder="Name" autocomplete="off" value="${data.athlete}" onfocus="this.select()">
                        <button type="submit" class="btn btn-primary">Submit</button>
                    </div>
                    <p>Total: ${data.total}</p>
                </form>
            </div>`;

        eGui.querySelector('form')?.addEventListener('submit', this.onFormSubmit);
    }

    onFormSubmit(e) {
        e.preventDefault();
        const { params } = this;
        const { node } = params;

        const target = (e.target ).querySelector('input') ;

        if (target?.value) {
            node?.setDataValue('athlete', target.value);
            if (this.params.hideTooltipCallback) {
                this.params.hideTooltipCallback();
            }
        }
    }

    getGui() {
        return this.eGui;
    }

    destroy() {
        this.eGui.querySelector('form')?.removeEventListener('submit', this.onFormSubmit);
    }
}
""")


columnDefs = [
    {
        "field": "athlete",
        "minWidth": 150,
        "tooltipField": "athlete",
        "tooltipComponentParams": {"type": "success"},
    },
    {"field": "age", "minWidth": 130, "tooltipField": "age"},
    {"field": "year"},
    {"field": "sport"},
]

grid_options = {
    "defaultColDef": {
        "flex": 1,
        "minWidth": 100,
        "tooltipComponent": CustomTooltip,
    },
    "tooltipInteraction": True,
    "tooltipShowDelay": 500,
    "columnDefs": columnDefs,
}


@st.cache_data()
def get_data():
    response = requests.get(
        "https://www.ag-grid.com/example-assets/olympic-winners.json"
    )
    return response.json()


data = pd.DataFrame(get_data())

AgGrid(data, gridOptions=grid_options, theme="streamlit", allow_unsafe_jscode=True)
