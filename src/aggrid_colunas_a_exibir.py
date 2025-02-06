import streamlit as st
from agstyler import PINLEFT, PRECISION_TWO
 
def colunas_aggrid(cBrowseName):
    
    if cBrowseName=='brw_df_totais_por_vendedores':
        cDictComColunasAgGrid = {
            'IDVENDEDOR': ('Vnd', {"pinned": "left", "width": 40, "filter":'agTextColumnFilter'}),         # ('Vnd', PINLEFT)  , filter='agTextColumnFilter'   o atributo pinned faz que a coluna fique fixa
            'NOME':       ('Nome', {'width': 80, "filter":'agTextColumnFilter'}),
            'FVAL':       ('Venda', {'width': 80}),
            'V_META':     ('Meta', {'width': 80}),
            'A1A2':       ('*', {'width': 30, "filter":'agTextColumnFilter'}),
            'TENDENCIA':  ('t', {'width': 30, "filter":'agTextColumnFilter'}),
            'QCLIPOSIT':  ('QtdCliPosit', {**PRECISION_TWO, 'width': 40}),
            'QCLICAD':    ('QtdCliCad', {**PRECISION_TWO, 'width': 40})
        }
    elif cBrowseName=='brw_df_totais_por_clientes':
        cDictComColunasAgGrid = {
            'IDCLI': ('Cli', {"pinned": "left", "width": 30, "filter":'agTextColumnFilter'}),         # ('Vnd', PINLEFT)  , filter='agTextColumnFilter'   o atributo pinned faz que a coluna fique fixa
            'NOMECLI': ('Nome', {'width': 80, "filter":'agTextColumnFilter'}),
            'FVAL': ('Venda', {'width': 60}),
            'A1A2': ('*', {'width': 30, "filter":'agTextColumnFilter'}),
            'TENDENCIA': ('t', {'width': 30, "filter":'agTextColumnFilter'})
        }
    
    else:
        cDictComColunasAgGrid = None

    # st.info(f""" cDictComColunasAgGrid ={cDictComColunasAgGrid } """)
    return cDictComColunasAgGrid 