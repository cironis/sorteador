import streamlit as st
from streamlit_gsheets import GSheetsConnection
import pandas as pd
from st_aggrid import AgGrid, GridOptionsBuilder

st.set_page_config(page_title="Board Game - Database", page_icon="♙", layout="wide")

@st.cache_data
def load_main_dataframe(worksheet):
    conn = st.connection("gsheets", type=GSheetsConnection)
    df = conn.read(worksheet=worksheet)
    return df

st.title("Database")

df = load_main_dataframe("database")

# Configure the 'thumbnail' column to use the built-in image renderer
gb = GridOptionsBuilder.from_dataframe(df)
gb.configure_column(
    'thumbnail',
    headerName='Image',
    cellRenderer='agImageCellRenderer',
    width=100,
    cellRendererParams={
        'width': 50,
        'height': 50
    }
)
gb.configure_column('name', headerName='Name')
gb.configure_column('year', headerName='Year')
gb.configure_column('minplayers', headerName='Min Players')
gb.configure_column('maxplayers', headerName='Max Players')
gb.configure_columns(['playingtime', 'url'], hide=True)
gb.configure_grid_options(
    getRowHeight=JsCode('function(params) { return 80; }')
)

# Define the onCellClicked event
on_cell_clicked = JsCode('''
function(event) {
    if (event.colDef.field === 'thumbnail') {
        window.open(event.data.url, '_blank');
    }
}
''')

gridOptions = gb.build()
gridOptions['onCellClicked'] = on_cell_clicked

# Display the grid
AgGrid(
    df,
    gridOptions=gridOptions,
    allow_unsafe_jscode=True
)
