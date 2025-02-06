from st_aggrid import AgGrid
from st_aggrid.grid_options_builder import GridOptionsBuilder
from st_aggrid.shared import GridUpdateMode, JsCode

MAX_TABLE_HEIGHT = 500


def get_numeric_style_with_precision(precision: int) -> dict:
    return {"type": ["numericColumn", "customNumericFormat"], "precision": precision}


PRECISION_ZERO = get_numeric_style_with_precision(0)
PRECISION_ONE = get_numeric_style_with_precision(1)
PRECISION_TWO = get_numeric_style_with_precision(2)
PINLEFT = {"pinned": "left"}


def draw_grid(
        df,
        formatter: dict = None,
        selection="multiple",
        use_checkbox=False,
        fit_columns=False,
        theme="streamlit",
        max_height: int = MAX_TABLE_HEIGHT,
        wrap_text: bool = False,
        auto_height: bool = False,
        grid_options: dict = None,
        key=None,
        css: dict = None
):

    gb = GridOptionsBuilder()
    gb.configure_default_column(
        filterable=True,
        groupable=False,
        editable=False,
        wrapText=wrap_text,
        autoHeight=auto_height
    )

    if grid_options is not None:
        gb.configure_grid_options(**grid_options)

    if not formatter is None:
        for latin_name, (cyr_name, style_dict) in formatter.items():
            gb.configure_column(latin_name, header_name=cyr_name, **style_dict)
            # gb.configure_column(latin_name, header_name=cyr_name, filter='agTextColumnFilter', **style_dict)

    # gb.configure_selection(selection_mode=selection, use_checkbox=use_checkbox)
    
    # gb.configure_pagination(paginationAutoPageSize=True)
    # gb.configure_side_bar()
    gridOptions=gb.build()
    # gridOptions['saveCellNavigation'] = {'saveButtonText': 'Aplicar Filtros'}
    # gridOptions['updateCellNavigation'] = {'updateCellNavigation': 'Aplicar Filtros'}  

    return AgGrid(
        df,
        gridOptions=gridOptions,
        update_mode=GridUpdateMode.VALUE_CHANGED,    # ele retornaria do aggrid se selecionar algo, ou editar algo, ou filtrar
        allow_unsafe_jscode=True,
        fit_columns_on_grid_load=fit_columns,
        height=min(max_height, (1 + len(df.index)) * 29),
        theme=theme,
        key=key,
        custom_css=css
    )
        # update_mode=GridUpdateMode.SELECTION_CHANGED | GridUpdateMode.VALUE_CHANGED | GridUpdateMode.FILTERING_CHANGED | GridUpdateMode.MANUAL,    # o normal usa: GridUpdateMode.FILTERING_CHANGED   pode ser tambem atraves de um botao tipo: GridUpdateMode.MANUAL

    # gb = GridOptionsBuilder.from_dataframe(df_totais_por_vendedores)
    # gb.configure_column('NOME', filter='agTextColumnFilter')
    # gb.configure_pagination(paginationAutoPageSize=True)
    # gb.configure_side_bar()
    
    # # Displaying the grid
    # grid_response = AgGrid(df_totais_por_vendedores, gridOptions=gb.build(), update_mode=GridUpdateMode.FILTERING_CHANGED, use_container_width=True)

def highlight(color, condition):
    code = f"""
        function(params) {{
            color = "{color}";
            if ({condition}) {{
                return {{
                    'backgroundColor': color
                }}
            }}
        }};
    """
    return JsCode(code)
