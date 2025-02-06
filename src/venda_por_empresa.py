import streamlit as st
import pandas as pd
import plotly.express as px
import streamlit_shadcn_ui as ui
import plotly.graph_objects as go
from streamlit_option_menu import option_menu
import numpy as np
from plotly.subplots import make_subplots
from plotly.subplots import make_subplots
# from firebase_admin import firestore
import myfunc
import os
st.set_option('deprecation.showPyplotGlobalUse', False)

def app():

    vendedores = myfunc.load_table('csv/vendedor.csv')
    clientes = myfunc.load_clientes( os.path.getmtime('csv/clientes.csv')  ) 
    vendas = myfunc.load_table('csv/venda.csv')
    relacao_vendedor = myfunc.load_table('csv/totvenda_vendedor.csv')


    mesclagem_vendedores = pd.merge(vendedores,vendas[['FVENDEDOR','FDATAEMI','FVAL','IDCLI']],left_on='IDVENDEDOR',right_on='FVENDEDOR')
    mesclagem_vendedores = mesclagem_vendedores.drop(columns='FVENDEDOR')

    cliente_vendedor = pd.merge(mesclagem_vendedores[['IDVENDEDOR','FVAL', 'IDCLI', 'NOME']], clientes[['IDCLI', 'NOMECLI', 'CIDADE', 'UF']], on='IDCLI')
    cliente_vendedor = cliente_vendedor.groupby(['IDCLI', 'NOMECLI', 'CIDADE', 'UF', 'IDVENDEDOR', 'NOME'])[['FVAL']].sum().reset_index()

    vendedor_clientes = pd.merge(relacao_vendedor[['IDVENDEDOR', 'QCLIPOSIT', 'QCLICAD', 'QCLIVISIT', 'V_META', 'FVAL','V_PROJ','QTDPRODCAD','QTDPROD']], vendedores, on='IDVENDEDOR')

    st.dataframe(vendedor_clientes)

    # Filtrando os dados para o vendedor selecionado
    total_clientes_cadastrados = vendedor_clientes['QCLICAD'].sum()
    total_clientes_compraram = vendedor_clientes['QCLIPOSIT'].sum()

    total_meta = vendedor_clientes['V_META'].sum()
    total_projetado = vendedor_clientes['V_PROJ']
    total_vendido = vendedor_clientes['FVAL']

    quantidade_cliente_visitados = vendedor_clientes['QCLIVISIT']

    total_prod_cadastrado = vendedor_clientes['QTDPRODCAD']
    total_prod_vendido = vendedor_clientes['QTDPROD']

