from pygwalker.api.streamlit import StreamlitRenderer
import streamlit as st
import pandas as pd
import myfunc
from st_aggrid import AgGrid, GridOptionsBuilder, GridUpdateMode
# import pygwalker as pyg
import os

st.set_option('deprecation.showPyplotGlobalUse', False)

def app():
    st.subheader('Crie seu gráfico para visualizar as métricas :bar_chart:', divider='rainbow')

    # Load data
    produtos = myfunc.load_produtos(os.path.getmtime('csv/produto.csv'))
    clientes = myfunc.load_table('csv/cliente.csv')
    venda_itens = myfunc.load_venda_itens(os.path.getmtime('csv/venda_itens.csv'))
    # Load vendedores with correct separator
    vendedores = pd.read_csv('csv/vendedores.csv', sep=';')
    vendas = myfunc.load_table('csv/venda.csv')
    

    # Perform merge operations
    venda_idpedido = pd.merge(venda_itens[['IDPEDIDO', 'PCOD', 'QTDVENDA', 'VLVENDA']], 
                              vendas[['IDPEDIDO', 'IDCLI', 'FVAL', 'FDESCONTO', 'FVENDEDOR']], on='IDPEDIDO')
    venda_cliente = pd.merge(venda_idpedido, clientes[['IDCLI', 'NOMECLI', 'CIDADE', 'UF']], on='IDCLI')
    venda_vendedor = pd.merge(venda_cliente, vendedores, left_on='FVENDEDOR', right_on='IDVENDEDOR', how='left')
    venda_produtos = pd.merge(venda_vendedor, produtos[['PCOD', 'PREF', 'PDESC', 'PUNIDADE', 'SALDO']], on='PCOD')

    # Drop the 'IDPEDIDO' column and group by the necessary columns
    venda_produtos = venda_produtos.drop(columns=['IDPEDIDO'])
    venda_produtos = venda_produtos.groupby(['PCOD', 'PDESC', 'PREF', 'PUNIDADE', 'SALDO', 
                                             'IDCLI', 'NOMECLI', 'CIDADE', 'UF', 
                                             'IDVENDEDOR', 'NOME'])[['QTDVENDA', 'VLVENDA']].sum().reset_index()

    # Display the dataframe using AgGrid for interactive table
    gb = GridOptionsBuilder.from_dataframe(venda_produtos)
    gb.configure_pagination(paginationAutoPageSize=True)
    gb.configure_side_bar()
    gb.configure_selection('single')
    gridOptions = gb.build()

    grid_response = AgGrid(
        venda_produtos,
        gridOptions=gridOptions,
        update_mode=GridUpdateMode.SELECTION_CHANGED,
        theme='alpine',
        enable_enterprise_modules=True,
        height=400,
        width='100%',
    )

    selected_rows = pd.DataFrame(grid_response['selected_rows'])
    
    if not selected_rows.empty:
        st.write("Selected Rows")
        st.write(selected_rows)
    
    # Allow user to create graph with pygwalker
    st.subheader('Visualize Data with Pygwalker')

    pyg_app = StreamlitRenderer(venda_produtos)

    pyg_app.explorer()